from dataclasses import dataclass
import logging
from src.domain.bot.exception import BotNotFoundException
from src.domain.user.entity import UserEntity
from src.domain.bot.entity import BotEntity
from src.infrastructure.repositories.bot.base import BaseBotRepository
from src.infrastructure.taskiq.tasks import send_notification_for_admin


logger = logging.getLogger(__name__)


@dataclass
class DeleteBotUseCase:

    _bot_repository: BaseBotRepository

    async def execute(self, bot_id: int, admin: UserEntity) -> BotEntity:

        bot: BotEntity | None = await self._bot_repository.get_bot_with_rentals(bot_id=bot_id)

        if not bot:
            raise BotNotFoundException()
        
        bot.delete()
        deleted_bot: BotEntity = await self._bot_repository.update(bot_entity=bot)
        logger.info(f'Администратор: {admin.telegram_id.to_raw()} удалил бота: {bot.id}')
        await send_notification_for_admin.kiq(text=f'Администратор: {admin.telegram_id.to_raw()} удалил бота: {bot.id}')
        return deleted_bot