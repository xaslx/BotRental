from aiogram import Bot, Dispatcher
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from backend.src.bot.ioc import BotProvider
import asyncio
from backend.src.config import Config
from backend.src.bot.handlers.users.main import router as main_router
import logging
from backend.src.logger import setup_logger


logger = logging.getLogger(__name__)


async def on_startup():
    setup_logger()
    logger.info('Бот включен')
    

async def on_shutdown():
    logger.info('Бот выключен')


async def main() -> None:
    
    config = Config()

    bot_container: AsyncContainer = make_async_container(
        BotProvider(), context={Config: config}
    )
    dp: Dispatcher = await bot_container.get(Dispatcher)
    bot: Bot = await bot_container.get(Bot)
    dp.include_router(router=main_router)
    setup_dishka(router=dp, container=bot_container)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)


    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())