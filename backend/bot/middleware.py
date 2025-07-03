from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject
from dishka.async_container import AsyncContainer
from src.infrastructure.repositories.telegram.base import BaseTelegramRepository


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:   
        
        user = event.from_user

        if user:
            container: AsyncContainer = data['dishka_container']
            repository: BaseTelegramRepository = await container.get(BaseTelegramRepository)
            await repository.add_user_if_not_exists(telegram_id=user.id)

        return await handler(event, data)