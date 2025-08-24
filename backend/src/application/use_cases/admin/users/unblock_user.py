import logging
from dataclasses import dataclass

from src.domain.user.blocked_user import BlockedUserEntity
from src.domain.user.entity import UserEntity
from src.domain.user.exception import UserNotFoundException
from src.infrastructure.repositories.user.base import (
    BaseBlockedUserRepository,
    BaseUserRepository,
)
from src.infrastructure.taskiq.tasks import send_notification_for_admin

logger = logging.getLogger(__name__)


@dataclass
class UnblockUserUseCase:
    _user_repository: BaseUserRepository
    _blocked_user_repository: BaseBlockedUserRepository

    async def execute(self, telegram_id: int, admin: UserEntity) -> bool:
        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(
            telegram_id=telegram_id
        )

        if not user:
            raise UserNotFoundException()

        block: BlockedUserEntity = user.unblock()

        await self._blocked_user_repository.update(block=block)
        logger.info(
            f'Администратор: {admin.telegram_id.to_raw()} разблокировал пользователя: {user.telegram_id.to_raw()}'
        )
        await send_notification_for_admin.kiq(
            text=f'Администратор: {admin.telegram_id.to_raw()} разблокировал пользователя: {user.telegram_id.to_raw()}'
        )
        return True
