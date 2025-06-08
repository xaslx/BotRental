from dataclasses import dataclass
import logging

from fastapi import HTTPException, status
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.domain.user.entity import UserEntity
from src.infrastructure.broker_messages.rabbitmq.publisher import publish
from src.presentation.schemas.user import CheckCodeSchema
from src.application.services.code import SendCodeService, CheckCodeService
from datetime import datetime
from src.const import MOSCOW_TZ
from src.application.services.jwt import JWTService
from src.presentation.schemas.jwt_token import JWTToken


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
    _jwt_service: JWTService

    async def execute(self, telegram_id: int) -> tuple[UserEntity, JWTToken]:

        new_user: UserEntity = UserEntity.create_user(telegram_id=telegram_id)
        created_user: UserEntity = await self._user_repository.add(entity=new_user)
        
        logger.info(f'Новый пользователь {telegram_id} зарегистрирован')
        await publish(
            chat_id=telegram_id,
            text=f'Вы успешно зарегистрировались на сервисе BotRental\n{
                datetime.strftime(new_user.created_at, '%d.%m.%Y %H:%M')
            }'
        )
        logger.info(f'Пользователю {telegram_id} направлено уведомление в Telegram')
        access_token, refresh_token = self._jwt_service.create_tokens(data={'sub': str(created_user.telegram_id.to_raw())})
        tokens: JWTToken = JWTToken(access_token=access_token, refresh_token=refresh_token)
        return created_user, tokens.access_token, tokens.refresh_token



@dataclass
class SendCodeUseCase:
    _send_code_service: SendCodeService

    async def execute(self, telegram_id: int) -> None:
        await self._send_code_service.execute(telegram_id=telegram_id)


@dataclass
class VerifyCodeUseCase:
    _check_code: CheckCodeService
    _login_use_case: LoginUserUseCase
    _register_use_case: RegisterUserUseCase
    _user_repository: BaseUserRepository

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
            
            await publish(
                chat_id=user.telegram_id.to_raw(),
                text=f'Вы успешно вошли на сервис BotRental\n{datetime.strftime(current_datetime, '%d.%m.%Y %H:%M')}'
            )
            logger.info(f'Пользователю {user.telegram_id.to_raw()} направлено уведомление в Telegram')
            return user, access_token, refresh_token
        
        return await self._register_use_case.execute(telegram_id=schema.telegram_id)
    

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
