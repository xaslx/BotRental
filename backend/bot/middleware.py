from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.async_container import AsyncContainer
from src.infrastructure.repositories.telegram.base import BaseTelegramRepository


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = event.from_user

        if user:
            container: AsyncContainer = data['dishka_container']
            repository: BaseTelegramRepository = await container.get(
                BaseTelegramRepository
            )
            await repository.add_user_if_not_exists(telegram_id=user.id)

        return await handler(event, data)
