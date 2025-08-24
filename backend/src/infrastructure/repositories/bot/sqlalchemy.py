import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.domain.bot.entity import BotEntity
from src.infrastructure.database.models.bots import Bot, BotRental
from src.infrastructure.repositories.bot.base import BaseBotRepository

logger = logging.getLogger(__name__)


@dataclass
class SQLAlchemyBotRepository(BaseBotRepository):
    _session: AsyncSession

    async def add(self, bot: BotEntity) -> BotEntity:
        try:
            model: Bot = Bot.from_entity(entity=bot)
            self._session.add(model)
            await self._session.commit()
            return model.to_entity()
        except Exception:
            raise

    async def get_all_bots(self) -> list[BotEntity] | None:
        try:
            result = await self._session.execute(select(Bot))
            bots: list[Bot] = result.scalars().all()
            if not bots:
                return None
            return [bot.to_entity(include_rentals=False) for bot in bots]
        except Exception as e:
            logger.error(f'Ошибка при получении всех ботов: {e}', exc_info=True)
            raise

    async def get_bot_by_id(self, bot_id: int) -> BotEntity | None:
        try:
            result = await self._session.execute(select(Bot).where(Bot.id == bot_id))
            bot = result.scalar_one_or_none()
            if not bot:
                return None
            return bot.to_entity(include_rentals=False)
        except Exception as e:
            logger.error(f'Ошибка при получении всех ботов: {e}', exc_info=True)
            raise

    async def get_all_bots_with_rentals(self) -> list[BotEntity] | None:
        try:
            result = await self._session.execute(
                select(Bot).options(
                    selectinload(Bot.rentals).selectinload(BotRental.user)
                )
            )
            bots: list[Bot] = result.scalars().all()
            if not bots:
                return None
            return [bot.to_entity() for bot in bots]
        except Exception as e:
            logger.error(
                f'Ошибка при получении ботов с арендаторами: {e}', exc_info=True
            )
            raise

    async def get_bot_with_rentals(self, bot_id: int) -> BotEntity | None:
        try:
            result = await self._session.execute(
                select(Bot)
                .where(Bot.id == bot_id)
                .options(selectinload(Bot.rentals).selectinload(BotRental.user))
            )
            bot = result.scalar_one_or_none()
            return bot.to_entity() if bot else None
        except Exception as e:
            logger.error(
                f'Ошибка при получении бота с арендаторами id={bot_id}: {e}',
                exc_info=True,
            )
            raise

    async def update(self, bot_entity: BotEntity) -> BotEntity | None:
        try:
            result = await self._session.execute(
                select(Bot)
                .where(Bot.id == bot_entity.id)
                .options(selectinload(Bot.rentals).selectinload(BotRental.user))
            )
            bot: Bot | None = result.scalar_one_or_none()

            if bot is None:
                msg = f'Бот с id={bot_entity.id} не найден.'
                logger.error(msg)
                return None

            bot.name = bot_entity.name.to_raw()
            bot.description = bot_entity.description.to_raw()
            bot.price = bot_entity.price.to_raw()
            bot.is_available = bot_entity.is_available
            bot.is_deleted = bot_entity.is_deleted
            bot = bot.to_entity()
            await self._session.commit()
            return bot

        except Exception as e:
            logger.error(
                f'Неизвестная ошибка при обновлении бота с id={bot_entity.id}: {e}',
                exc_info=True,
            )
            raise
