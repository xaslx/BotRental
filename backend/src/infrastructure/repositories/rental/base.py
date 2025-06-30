from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.domain.bot.entity import BotRentalEntity


@dataclass
class BaseRentalRepository(ABC):

    @abstractmethod
    async def add(self, rental: BotRentalEntity) -> BotRentalEntity:
        ...

    @abstractmethod
    async def get_by_id(self, rental_id: int) -> BotRentalEntity | None:
        ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[BotRentalEntity]:
        ...