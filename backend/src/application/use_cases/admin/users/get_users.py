import logging
from dataclasses import dataclass

from src.domain.user.entity import UserEntity
from src.domain.user.exception import UserNotFoundException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.taskiq.tasks import send_notification_for_admin

logger = logging.getLogger(__name__)


@dataclass
class GetAllUsersUseCase:
    _user_repository: BaseUserRepository

    async def execute(self, admin: UserEntity) -> list[UserEntity] | None:
        users: list[UserEntity] | None = await self._user_repository.get_all_users()

        if not users:
            return None

        logger.info(
            f'Администратор {admin.telegram_id.value} получил список пользователей'
        )
        await send_notification_for_admin.kiq(
            text=f'Администратор {admin.telegram_id.value} получил список пользователей'
        )

        return users


@dataclass
class GetUserByTelegramId:
    _user_repository: BaseUserRepository

    async def execute(self, telegram_id: int, admin: UserEntity) -> UserEntity | None:
        user: (
            UserEntity | None
        ) = await self._user_repository.get_full_user_info_for_admin(
            telegram_id=telegram_id
        )

        if not user:
            raise UserNotFoundException()

        logger.info(
            f'Администратор {admin.telegram_id.to_raw()} получил пользователя: {user.telegram_id.to_raw()}'
        )
        await send_notification_for_admin.kiq(
            text=f'Администратор {admin.telegram_id.to_raw()} получил пользователя: {user.telegram_id.to_raw()}'
        )
        return user
