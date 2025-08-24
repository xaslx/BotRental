import logging
from dataclasses import dataclass

from src.domain.user.entity import UserEntity
from src.domain.user.exception import PermissionDeniedException, UserNotFoundException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.taskiq.tasks import send_notification_for_admin

logger = logging.getLogger(__name__)


@dataclass
class DeleteUserUseCase:
    _user_repository: BaseUserRepository

    async def execute(self, telegram_id: int, admin: UserEntity) -> UserEntity | None:
        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(
            telegram_id=telegram_id
        )

        if not user:
            raise UserNotFoundException()

        if user.telegram_id.to_raw() == admin.telegram_id.to_raw():
            logger.warning(
                f'Администратор: {admin.telegram_id.to_raw()} попытался удалить сам себя'
            )
            await send_notification_for_admin.kiq(
                text=f'Администратор: {admin.telegram_id.to_raw()} попытался удалить сам себя'
            )
            raise PermissionDeniedException()

        if user.role in ['dev', 'admin']:
            logger.warning(
                f'Администратор: {admin.telegram_id.to_raw()} попытался удалить администратора: {user.telegram_id.to_raw()}'
            )
            await send_notification_for_admin.kiq(
                text=f'Администратор: {admin.telegram_id.to_raw()} попытался удалить администратора: {user.telegram_id.to_raw()}'
            )
            raise PermissionDeniedException()

        if not user.is_deleted:
            user.delete()
            deleted_user: UserEntity = await self._user_repository.update(entity=user)
            logger.info(
                f'Администратор: {admin.telegram_id.to_raw()} удалил пользователя: {user.telegram_id.to_raw()}'
            )
            await send_notification_for_admin.kiq(
                text=f'Администратор: {admin.telegram_id.to_raw()} удалил пользователя: {user.telegram_id.to_raw()}'
            )
            return deleted_user
