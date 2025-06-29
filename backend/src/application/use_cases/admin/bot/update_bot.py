import logging
from dataclasses import dataclass

from src.domain.bot.entity import BotEntity
from src.domain.bot.exception import BotNotFoundException
from src.domain.user.entity import UserEntity
from src.infrastructure.repositories.bot.base import BaseBotRepository
from src.presentation.schemas.bot import UpdateBotSchema


logger = logging.getLogger(__name__)


@dataclass
class UpdateBotUseCase:

    _bot_repository: BaseBotRepository

    async def execute(self, bot_id: int, admin: UserEntity, update_schema: UpdateBotSchema) -> BotEntity:

        bot: BotEntity | None = await self._bot_repository.get_bot_with_rentals(bot_id=bot_id)
        
        if not bot:
            raise BotNotFoundException()

        bot.update(
            name=update_schema.name,
            description=update_schema.description,
            price=update_schema.price,
        )

        updated_bot: BotEntity = await self._bot_repository.update(bot_entity=bot)
        logger.info(f'Администратор: {admin.telegram_id.to_raw()} обновил бота: {bot.id} -> ({update_schema})')
        return updated_bot
    

        


