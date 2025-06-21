from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from src.domain.bot.entity import BotEntity
from src.infrastructure.database.models.base import Base


T = TypeVar('T', bound=Base)


@dataclass
class BaseBotRepository(ABC, Generic[T]):
    
    @abstractmethod
    async def add(self, bot: BotEntity) -> BotEntity:
        ...

    @abstractmethod
    async def get_all_bots(self) -> list[BotEntity] | None:
        ...

    @abstractmethod
    async def get_bot_by_id(self, bot_id: int) -> BotEntity | None:
        ...

    @abstractmethod
    async def update(self, bot: BotEntity) -> BotEntity | None:
        ...