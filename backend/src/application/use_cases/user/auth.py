import logging
from dataclasses import dataclass
from datetime import datetime

from fastapi import HTTPException, status
from src.application.services.code import CheckCodeService, SendCodeService
from src.application.services.jwt import JWTService
from src.const import MOSCOW_TZ
from src.domain.referral.entity import ReferralEntity
from src.domain.user.entity import UserEntity
from src.domain.user.exception import ReferrerNotFoundException
from src.infrastructure.cache.base import BaseCacheService
from src.infrastructure.repositories.referral.base import \
    BaseReferralRepository
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.taskiq.tasks import send_notification
from src.presentation.schemas.jwt_token import JWTToken
from src.presentation.schemas.user import CheckCodeSchema


logger = logging.getLogger(__name__)


@dataclass
class LoginUserUseCase:
    _user_repository: BaseUserRepository
    _jwt_service: JWTService

    async def execute(self, user: UserEntity) -> tuple[UserEntity, JWTToken]:

        access_token, refresh_token = self._jwt_service.create_tokens(
            data={'sub': str(user.telegram_id.to_raw())}
        )
        tokens: JWTToken = JWTToken(access_token=access_token, refresh_token=refresh_token)
        return user, tokens.access_token, tokens.refresh_token


@dataclass
class RegisterUserUseCase:
    _user_repository: BaseUserRepository
    _referral_repository: BaseReferralRepository
    _jwt_service: JWTService
    _cache_service: BaseCacheService

    async def execute(self, telegram_id: int, ref_id: int | None = None) -> tuple[UserEntity, JWTToken]:
        new_user: UserEntity = UserEntity.create_user(telegram_id=telegram_id)

        if ref_id:
            referrer_user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(telegram_id=ref_id)
            if not referrer_user:
                logger.warning(f'Реферер с telegram_id={ref_id} не найден')
                await self._cache_service.delete(key=f'{new_user.telegram_id.to_raw()}:referral')
                raise ReferrerNotFoundException()
            new_user.assign_referrer(referrer_id=referrer_user.id)
            new_user.add_welcome_bonus()

        created_user: UserEntity = await self._user_repository.add(entity=new_user)

        if ref_id:
            referral: ReferralEntity = ReferralEntity.create_referral(
                referrer_id=referrer_user.id,
                referral_id=created_user.id,
                telegram_id=new_user.telegram_id.to_raw()
            )
            await self._referral_repository.add(referral)
            await self._cache_service.delete(key=f'{new_user.telegram_id.to_raw()}:referral')

        logger.info(f'Новый пользователь {telegram_id} зарегистрирован')
        await send_notification.kiq(
            user_id=telegram_id,
            text=f'Вы успешно зарегистрировались на сервисе BotRental\n{datetime.strftime(new_user.created_at, "%d.%m.%Y %H:%M")}'
        )
        logger.info(f'Пользователю {telegram_id} направлено уведомление в Telegram')

        access_token, refresh_token = self._jwt_service.create_tokens(data={'sub': str(created_user.telegram_id.to_raw())})
        tokens: JWTToken = JWTToken(access_token=access_token, refresh_token=refresh_token)
        return created_user, tokens.access_token, tokens.refresh_token


@dataclass
class SendCodeUseCase:
    _send_code_service: SendCodeService

    async def execute(self, telegram_id: int, ref_id: int | None = None) -> None:
        await self._send_code_service.execute(telegram_id=telegram_id, ref_id=ref_id)


@dataclass
class VerifyCodeUseCase:
    _check_code: CheckCodeService
    _login_use_case: LoginUserUseCase
    _register_use_case: RegisterUserUseCase
    _user_repository: BaseUserRepository
    _cache_service: BaseCacheService

    async def execute(self, schema: CheckCodeSchema) -> tuple[UserEntity, JWTToken]:
        await self._check_code.execute(
            code=schema.confirmation_code,
            telegram_id=schema.telegram_id
        )
        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(telegram_id=schema.telegram_id)

        if user:
            user, access_token, refresh_token = await self._login_use_case.execute(user=user)

            logger.info(f'Пользователь {user.telegram_id.to_raw()} совершил вход.')
            current_datetime = datetime.now(tz=MOSCOW_TZ)
            
            await send_notification.kiq(
                user_id=user.telegram_id.to_raw(),
                text=f'Вы успешно вошли на сервис BotRental\n{datetime.strftime(current_datetime, '%d.%m.%Y %H:%M')}',
            )
            
            logger.info(f'Пользователю {user.telegram_id.to_raw()} направлено уведомление в Telegram')
            return user, access_token, refresh_token
        
        ref_id_val: str | None = await self._cache_service.get(key=f'{schema.telegram_id}:referral')
        ref_id: int | None = int(ref_id_val) if ref_id_val is not None else None
        
        return await self._register_use_case.execute(telegram_id=schema.telegram_id, ref_id=ref_id)
    

@dataclass
class RefreshTokenUseCase:
    _jwt_service: JWTService

    async def execute(self, refresh_token: str) -> str:
        try:
            new_access_token: str | None = self._jwt_service.refresh_access_token(refresh_token)
            return new_access_token
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
