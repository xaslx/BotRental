import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.bot.entity import BotRentalEntity
from src.infrastructure.database.models.bots import BotRental
from src.infrastructure.repositories.rental.base import BaseRentalRepository

logger = logging.getLogger(__name__)


@dataclass
class SQLAlchemyRentalRepository(BaseRentalRepository):
    _session: AsyncSession

    async def add(self, rental: BotRentalEntity) -> BotRentalEntity:
        try:
            model = BotRental.from_entity(rental)
            self._session.add(model)
            await self._session.flush()
            rental.id = model.id
            logger.info(f'Добавлена аренда: {rental.to_dict()}')
            return rental
        except Exception:
            logger.exception(f'Ошибка при добавлении аренды: {rental}')
            raise

    async def get_by_id(self, rental_id: int) -> BotRentalEntity | None:
        try:
            result = await self._session.execute(
                select(BotRental).where(BotRental.id == rental_id)
            )
            rental = result.scalar_one_or_none()
            if rental:
                logger.info(f'Аренда найдена: id={rental_id}')
                return rental.to_entity(include_user=False)
            logger.info(f'Аренда не найдена: id={rental_id}')
            return None
        except Exception:
            logger.exception(f'Ошибка при получении аренды по id={rental_id}')
            raise

    async def get_all_by_user_id(self, user_id: int) -> list[BotRentalEntity]:
        try:
            result = await self._session.execute(
                select(BotRental).where(BotRental.user_id == user_id)
            )
            rentals = result.scalars().all()
            logger.info(f'Получено аренд: {len(rentals)}')
            return [rental.to_entity(include_user=False) for rental in rentals]
        except Exception:
            logger.exception('Ошибка при получении всех аренд')
            return []

    async def update(self, rental: BotRentalEntity) -> BotRentalEntity:
        try:
            result = await self._session.execute(
                select(BotRental).where(BotRental.id == rental.id)
            )
            model: BotRental | None = result.scalar_one_or_none()
            if not model:
                logger.warning(f'Аренда для обновления не найдена: id={rental.id}')
                return None

            model.is_active = rental.is_active
            model.rented_until = rental.rented_until
            model.token = rental.token

            logger.info(f'Аренда обновлена: {rental.to_dict()}')

            return rental
        except Exception:
            logger.exception(f'Ошибка при обновлении аренды: {rental}')
            raise
