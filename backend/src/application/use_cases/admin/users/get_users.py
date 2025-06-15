from dataclasses import dataclass
from src.domain.user.entity import UserEntity
from src.presentation.schemas.user import UserOutSchema
from src.infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class GetAllUsersUseCase:
    _user_repository: BaseUserRepository

    async def execute(self) -> list[UserOutSchema] | None:

        users: list[UserEntity] | None = await self._user_repository.get_all_users()
        if not users:
            return None
        return [UserOutSchema.model_validate(user) for user in users]



@dataclass
class GetUserByTelegramId:
    _user_repository: BaseUserRepository

    async def execute(self, telegram_id: int) -> UserOutSchema | None:

        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(telegram_id=telegram_id)

        if not user:
            return None
        
        return UserOutSchema.model_validate(user)