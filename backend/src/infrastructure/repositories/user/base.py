from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from src.domain.user.blocked_user import BlockedUserEntity
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.base import Base

T = TypeVar('T', bound=Base)


@dataclass
class BaseUserRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, entity: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None: ...

    @abstractmethod
    async def get_all_users(self) -> list[UserEntity] | None: ...

    @abstractmethod
    async def get_user_with_rentals(self, user_id: int) -> UserEntity | None: ...

    @abstractmethod
    async def update(self, entity: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def get_full_user_info_for_admin(
        self, telegram_id: int
    ) -> UserEntity | None: ...

    @abstractmethod
    async def delete(self, entity: UserEntity) -> None: ...


@dataclass
class BaseBlockedUserRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, block: BlockedUserEntity) -> None: ...

    @abstractmethod
    async def update(self, block: BlockedUserEntity) -> None: ...

    @abstractmethod
    async def get_active_block_by_user_id(
        self, user_id: int
    ) -> BlockedUserEntity | None: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[BlockedUserEntity]: ...
