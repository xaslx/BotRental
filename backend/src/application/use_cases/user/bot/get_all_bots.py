from dataclasses import dataclass

from src.domain.bot.entity import BotEntity
from src.infrastructure.repositories.bot.base import BaseBotRepository


@dataclass
class GetAllBotsUseCase:
    _bot_repository: BaseBotRepository

    async def execute(self) -> list[BotEntity] | None:
        return await self._bot_repository.get_all_bots()
