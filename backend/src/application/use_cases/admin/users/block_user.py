import logging
from dataclasses import dataclass

from src.domain.user.blocked_user import BlockedUserEntity
from src.domain.user.entity import UserEntity
from src.domain.user.exception import SelfBlockException, UserNotFoundException
from src.infrastructure.repositories.user.base import (
    BaseBlockedUserRepository,
    BaseUserRepository,
)
from src.infrastructure.taskiq.tasks import send_notification_for_admin
from src.presentation.schemas.user import UserBlockSchema

logger = logging.getLogger(__name__)


@dataclass
class BlockUserUseCase:
    _user_repository: BaseUserRepository
    _blocked_user_repository: BaseBlockedUserRepository

    async def execute(
        self, telegram_id: int, admin: UserEntity, block_schema: UserBlockSchema
    ) -> BlockedUserEntity:
        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(
            telegram_id=telegram_id
        )

        if not user:
            raise UserNotFoundException()

        if user.id == admin.id:
            logger.warning(
                f'Администратор: {admin.telegram_id.to_raw()} попытался заблокировать сам себя.'
            )
            await send_notification_for_admin.kiq(
                text=f'Администратор: {admin.telegram_id.to_raw()} попытался заблокировать сам себя.'
            )
            raise SelfBlockException()

        block: BlockedUserEntity = user.block(
            days=block_schema.days,
            reason=block_schema.reason,
            admin_id=admin.id,
        )

        await self._blocked_user_repository.add(block)
        logger.info(
            f'Администратор: {admin.telegram_id.to_raw()} заблокировал пользователя: {user.telegram_id.to_raw()}'
        )
        await send_notification_for_admin.kiq(
            text=f'Администратор: {admin.telegram_id.to_raw()} заблокировал пользователя: {user.telegram_id.to_raw()}'
        )
        return block
