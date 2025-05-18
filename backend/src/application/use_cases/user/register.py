from dataclasses import dataclass
from src.domain.user.exception import UserAlreadyExistsException
import logging
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.domain.user.entity import UserEntity
from src.infrastructure.broker_messages.rabbitmq.publisher import publish
from src.presentation.schemas.user import CheckCodeSchema, RegisterUserSchema
from src.infrastructure.cache.base import BaseCacheService
from src.application.services.code import SendCodeService, CheckCodeService



logger = logging.getLogger(__name__)


@dataclass
class NewUserUseCase:
    user_repository: BaseUserRepository
    cache_service: BaseCacheService
    send_code_service: SendCodeService

    async def execute(self, new_user: RegisterUserSchema) -> UserEntity:
        
        user: UserEntity | None = await self.user_repository.get_user_by_telegram_id(telegram_id=new_user.telegram_id)
        logger.info(f'Поиск пользователя в базе по telegram_id: {new_user.telegram_id}')

        if user:
            logger.info(f'Пользователь: {new_user.telegram_id} найден в базе данных')
            raise UserAlreadyExistsException()
        
        await self.send_code_service.execute(telegram_id=new_user.telegram_id)


@dataclass
class RegisterUserUseCase:
    check_code: CheckCodeService
    user_repository: BaseUserRepository

    async def execute(self, schema: CheckCodeSchema) -> UserEntity | None:
        res: bool = await self.check_code.execute(code=schema.confirmation_code, telegram_id=schema.telegram_id)

        if res:
            new_user: UserEntity = UserEntity.create_user(
                telegram_id=schema.telegram_id,
            )
            
            user: UserEntity = await self.user_repository.add(entity=new_user)
            logger.info(f'Новый пользователь: {new_user.telegram_id} добавлен в базу данных')

            await publish(
                chat_id=new_user.telegram_id.to_raw(),
                text=f'Вы успешно зарегистрировались на сервисе BotRental и привязали свой Телеграм.')
            
            logger.info(f'Пользователю: {new_user.telegram_id} направлено уведомление в Телеграм о успешной регистрации')
            return user
        
        logger.error(f'Не удалост добавить нового пользователя: Telegram ID: {schema.telegram_id}')
        return None