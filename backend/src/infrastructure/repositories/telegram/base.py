from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class BaseTelegramRepository:
    @abstractmethod
    async def add_user_if_not_exists(self, telegram_id: int): ...

    @abstractmethod
    async def get_all_users(self): ...
