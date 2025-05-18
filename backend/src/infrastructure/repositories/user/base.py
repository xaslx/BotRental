from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.base import Base


T = TypeVar('T', bound=Base)


@dataclass
class BaseUserRepository(ABC, Generic[T]):

    @abstractmethod
    async def add(self, entity: UserEntity) -> UserEntity:
        ...


    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:
        ...


    @abstractmethod
    async def update(self, entity: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    async def delete(self, entity: UserEntity) -> None:
        ...