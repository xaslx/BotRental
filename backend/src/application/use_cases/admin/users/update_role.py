from dataclasses import dataclass
import logging
from src.presentation.schemas.user import UpdateUserRole
from src.domain.user.entity import UserEntity, Role
from src.domain.user.exception import UserNotFoundException, PermissionDeniedException
from src.infrastructure.repositories.user.base import BaseUserRepository


logger = logging.getLogger(__name__)


@dataclass
class UpdateUserRoleUseCase:
    _user_repository: BaseUserRepository

    async def execute(self, telegram_id: int, admin: UserEntity, new_role: UpdateUserRole) -> UserEntity:
        
        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(telegram_id=telegram_id)

        if not user:
            raise UserNotFoundException()
        
        if user.telegram_id.to_raw() == admin.telegram_id.to_raw():
            logger.warning(f'Администратор: {admin.telegram_id.to_raw()} попытался сменить роль сам себе')
            raise PermissionDeniedException()
        
        if user.role == Role.DEV:
            logger.warning(f'Администратор: {admin.telegram_id.to_raw()} попытался сменить роль у разработчика: {user.telegram_id.to_raw()}')
            raise PermissionDeniedException()
        
        old_role: Role = user.role

        if user.role != new_role.role:

            user.change_role(new_role=new_role.role)
            await self._user_repository.update(entity=user)
            logger.info(
                f'Администратор: {admin.telegram_id.to_raw()} сменил роль пользователю: {user.telegram_id.to_raw()} ({old_role} -> {new_role.role})'
            )

        return user
        
        
