from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.bot.entity import BotRentalEntity
from src.domain.bot.exception import RentalNotFoundException
from src.domain.user.entity import UserEntity
from src.domain.user.exception import PermissionDeniedException
from src.infrastructure.repositories.rental.base import BaseRentalRepository


@dataclass
class StopBotRentalUseCase:
    _rental_repository: BaseRentalRepository
    _session: AsyncSession

    async def execute(self, rental_id: int, user: UserEntity) -> bool:
        rental: BotRentalEntity | None = await self._rental_repository.get_by_id(
            rental_id=rental_id
        )

        if not rental:
            raise RentalNotFoundException()

        if rental.user_id != user.id:
            raise PermissionDeniedException()

        rental.stop()

        await self._rental_repository.update(rental=rental)

        await self._session.commit()

        return True
