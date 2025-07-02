from dataclasses import dataclass
from src.infrastructure.cache.base import BaseCacheService
import random
from abc import ABC
import logging
from src.infrastructure.taskiq.tasks import send_notification
from src.domain.user.exception import InvalidCodeException, TooManyCodeRequestsException


logger = logging.getLogger(__name__)


async def send_and_cache(telegram_id: int, cache_service: BaseCacheService) -> bool:

    code: str = str(random.randint(100000, 999999))
    logger.info(f'Сгенерирован код: {code} для пользователя: {telegram_id}')

    await send_notification.kiq(user_id=telegram_id, text=f'Ваш код: {code}')
    logger.info(f'Код: {code} отправлен пользователю в телеграм: {telegram_id}')

    await cache_service.set_with_ttl(key=f'{telegram_id}:code', value=code, ttl_seconds=300)
    logger.info(f'Код записан в редис')

    return True


@dataclass
class SendCodeService(ABC):
    _cache_service: BaseCacheService

    async def execute(self, telegram_id: int, ref_id: int | None = None) -> bool:
        code: str = await self._cache_service.get(f'{telegram_id}:code')

        if code:
            raise TooManyCodeRequestsException()
        
        if ref_id:
            await self._cache_service.set_with_ttl(
                key=f'{telegram_id}:referral',
                value=str(ref_id),
                ttl_seconds=300,
            )
        
        return await send_and_cache(telegram_id=telegram_id, cache_service=self._cache_service)


@dataclass
class CheckCodeService: 
    _cache_service: BaseCacheService

    async def execute(self, code: int, telegram_id: int) -> bool:

        cache_code: str | None = await self._cache_service.get(key=f'{telegram_id}:code')
        logger.info(f'Получение кода из кэша, для пользователя: {telegram_id}: код: {cache_code}')
        
        if not cache_code or int(cache_code) != code:
            logger.warning(f'Неверный код для пользователя {telegram_id}')
            raise InvalidCodeException()
        
        logger.info(f'Успешная проверка кода: {code} для пользователя: {telegram_id}')

        await self._cache_service.delete(key=f'{telegram_id}:code')
        logger.info(f'Код из кэша для пользователя: {telegram_id} удален')

        return True
        