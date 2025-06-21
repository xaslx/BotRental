from src.infrastructure.repositories.bot.base import BaseBotRepository
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.database.models.bots import Bot
from src.domain.bot.entity import BotEntity
import logging


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
        except Exception as e:
            raise

    async def get_all_bots(self):
        return await super().get_all_bots()
    
    async def get_bot_by_id(self, bot_id):
        return await super().get_bot_by_id(bot_id)
    
    async def update(self, bot_entity: BotEntity) -> BotEntity | None:
        try:
            result = await self._session.execute(
                select(Bot).where(Bot.id == bot_entity.id)
            )
            bot: Bot | None = result.scalar_one_or_none()

            if bot is None:
                msg = f'Бот с id={bot_entity.id} не найден.'
                logger.error(msg)
                return None

            bot.name = bot_entity.name
            bot.description = bot_entity.description
            bot.price = bot_entity.price
            bot.is_available = bot_entity.is_available
            bot.is_deleted = bot_entity.is_deleted

            await self._session.commit()
            return bot.to_entity()

        except Exception as e:
            logger.error(f'Неизвестная ошибка при обновлении бота с id={bot_entity.id}: {e}', exc_info=True)
            raise