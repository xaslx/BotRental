from dataclasses import dataclass

from src.domain.bot.entity import BotRentalEntity
from src.infrastructure.repositories.rental.base import BaseRentalRepository


@dataclass
class GetUserRentalsUseCase:
    _rental_repository: BaseRentalRepository

    async def execute(self, user_id: int) -> list[BotRentalEntity]:
        return await self._rental_repository.get_all_by_user_id(user_id=user_id)
