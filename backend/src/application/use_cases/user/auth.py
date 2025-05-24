from dataclasses import dataclass
import logging
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.domain.user.entity import UserEntity
from src.infrastructure.broker_messages.rabbitmq.publisher import publish
from src.presentation.schemas.user import CheckCodeSchema
from src.application.services.code import SendCodeService, CheckCodeService
from datetime import datetime
from src.const import MOSCOW_TZ


logger = logging.getLogger(__name__)


@dataclass
class LoginUserUseCase:
    _user_repository: BaseUserRepository

    async def execute(self, telegram_id: int) -> UserEntity | None:

        return await self._user_repository.get_user_by_telegram_id(telegram_id)


@dataclass
class RegisterUserUseCase:
    _user_repository: BaseUserRepository

    async def execute(self, telegram_id: int) -> UserEntity:

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
        return created_user



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

    async def execute(self, schema: CheckCodeSchema) -> UserEntity:

        await self._check_code.execute(
            code=schema.confirmation_code,
            telegram_id=schema.telegram_id
        )


        user: UserEntity | None = await self._login_use_case.execute(schema.telegram_id)

        if user:
            logger.info(f'Пользователь {user.telegram_id.to_raw()} совершил вход.')
            current_datetime: datetime = datetime.now(tz=MOSCOW_TZ)

            await publish(
                chat_id=user.telegram_id.to_raw(),
                text=f'Вы успешно вошли на сервис BotRental\n{datetime.strftime(current_datetime, '%d.%m.%Y %H:%M')}'
            )
            logger.info(f'Пользователю {user.telegram_id.to_raw()} направлено уведомление в Telegram')
            return user
        
        return await self._register_use_case.execute(schema.telegram_id)