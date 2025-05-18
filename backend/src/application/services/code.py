from dataclasses import dataclass
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.cache.base import BaseCacheService
import random
from src.infrastructure.broker_messages.rabbitmq.publisher import publish
from abc import ABC
import logging
from src.domain.user.exception import InvalidCodeError



logger = logging.getLogger(__name__)


async def send_and_cache(telegram_id: int, cache_service: BaseCacheService) -> bool:

    code: str = str(random.randint(100000, 999999))
    logger.info(f'Сгенерирован код: {code} для пользователя: {telegram_id}')

    await publish(chat_id=telegram_id, text=f'Ваш код: {code}')
    logger.info(f'Код: {code} отправлен пользователю в телеграм: {telegram_id}')

    await cache_service.set_with_ttl(key=f'{telegram_id}:code', value=code, ttl_seconds=600)
    logger.info(f'Код записан в редис')

    return True


@dataclass
class SendCodeService(ABC):
    user_repository: BaseUserRepository
    cache_service: BaseCacheService

    async def _check_user(self, telegram_id: int) -> bool:
        return await self.user_repository.get_user_by_telegram_id(telegram_id=telegram_id)
    
    async def execute(self, telegram_id: int) -> bool:
        return await send_and_cache(telegram_id=telegram_id, cache_service=self.cache_service)


@dataclass
class CheckCodeService:
    cache_service: BaseCacheService

    async def execute(self, code: int, telegram_id: int) -> bool:

        cache_code = await self.cache_service.get(key=f'{telegram_id}:code')
        logger.info(f'Получение кода из кэша, для пользователя: {telegram_id}: код: {cache_code}')

        if not cache_code:
            logger.warning(f'Не удалось найти код в редисе, для пользователя: {telegram_id}')
            raise InvalidCodeError()
        
        if int(cache_code) != code:
            logger.warning(f'Пользователь: {telegram_id} ввел неверный код: {code}')
            raise InvalidCodeError()
        
        logger.info(f'Успешная проверка кода: {code} для пользователя: {telegram_id}')

        await self.cache_service.delete(key=f'{telegram_id}:code')
        logger.info(f'Код из кэша для пользователя: {telegram_id} удален')

        return True
        