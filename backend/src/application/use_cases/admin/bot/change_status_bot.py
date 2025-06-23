from dataclasses import dataclass
from typing import Callable
import logging
from src.domain.bot.entity import BotEntity
from src.domain.bot.exception import BotNotFoundException
from src.domain.user.entity import UserEntity
from src.infrastructure.repositories.bot.base import BaseBotRepository


logger = logging.getLogger(__name__)


@dataclass
class BaseBotStatusUseCase:
    _bot_repository: BaseBotRepository

    async def _change_bot_status(
        self,
        bot_id: int,
        admin: UserEntity,
        status_action: Callable[[BotEntity], None],
        action_name: str,
    ) -> BotEntity:
        
        bot: BotEntity | None = await self._bot_repository.get_bot_with_rentals(bot_id=bot_id)
        
        if not bot:
            raise BotNotFoundException()
        
        status_action(bot)
        updated_bot = await self._bot_repository.update(bot_entity=bot)
        
        logger.info(
            f'Администратор: {admin.telegram_id.to_raw()} {action_name} бота: {bot.id}'
        )
        return updated_bot


@dataclass
class ActivateBotUseCase(BaseBotStatusUseCase):
    async def execute(self, bot_id: int, admin: UserEntity) -> BotEntity:
        return await self._change_bot_status(
            bot_id=bot_id,
            admin=admin,
            status_action=lambda bot: bot.activate(),
            action_name='активировал',
        )


@dataclass
class DeactivateBotUseCase(BaseBotStatusUseCase):
    async def execute(self, bot_id: int, admin: UserEntity) -> BotEntity:
        return await self._change_bot_status(
            bot_id=bot_id,
            admin=admin,
            status_action=lambda bot: bot.deactivate(),
            action_name='деактивировал',
        )