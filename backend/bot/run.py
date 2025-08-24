import asyncio
import logging

from aiogram import Bot, Dispatcher
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from src.config import Config
from src.infrastructure.taskiq.broker import broker
from src.logger import setup_logger

from .handlers.admins.handlers import router as admins_router
from .handlers.users.handlers import router as users_router
from .ioc import BotProvider
from .middleware import UserCheckMiddleware

logger = logging.getLogger(__name__)


async def on_startup():
    setup_logger()
    logger.info('Бот включен')
    await broker.startup()


async def on_shutdown():
    logger.info('Бот выключен')
    await broker.shutdown()


async def main() -> None:
    config: Config = Config()

    bot_container: AsyncContainer = make_async_container(
        BotProvider(), context={Config: config}
    )
    dp: Dispatcher = await bot_container.get(Dispatcher)
    bot: Bot = await bot_container.get(Bot)
    dp.include_router(router=admins_router)
    dp.include_router(router=users_router)
    dp.message.middleware(UserCheckMiddleware())
    setup_dishka(router=dp, container=bot_container)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
