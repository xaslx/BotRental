from collections.abc import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.config import Config
from src.infrastructure.database.postgresql import new_session_maker
from src.infrastructure.repositories.telegram.base import BaseTelegramRepository
from src.infrastructure.repositories.telegram.sqlalchemy import (
    SQLAlchemyTelegramRepository,
)


class BotProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_bot(self, config: Config) -> Bot:
        return Bot(
            token=config.telegram.token, default=DefaultBotProperties(parse_mode='HTML')
        )

    @provide(scope=Scope.APP)
    def get_dispatcher(self) -> Dispatcher:
        return Dispatcher()

    # repo
    @provide(scope=Scope.REQUEST)
    def get_telegram_repository(self, session: AsyncSession) -> BaseTelegramRepository:
        return SQLAlchemyTelegramRepository(_session=session)
