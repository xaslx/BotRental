import logging
from dataclasses import dataclass

from src.domain.bot.entity import BotEntity
from src.domain.user.entity import UserEntity
from src.infrastructure.repositories.bot.base import BaseBotRepository
from src.presentation.schemas.bot import CreateBotSchema


logger = logging.getLogger(__name__)


@dataclass
class CreateNewBotUseCase:
    _bot_repository: BaseBotRepository

    async def execute(self, bot: CreateBotSchema, admin: UserEntity) -> BotEntity:

        new_bot: BotEntity = BotEntity.create_bot(name=bot.name, description=bot.description, price=bot.price)
        bot: BotEntity = await self._bot_repository.add(bot=new_bot)
        logger.info(f'Администратор: {admin.telegram_id.to_raw()} добавил нового бота: {bot}')
        return bot