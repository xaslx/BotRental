from aiogram import Bot, Dispatcher
from dishka import Provider, Scope, provide, from_context
from backend.src.config import Config
from aiogram.client.default import DefaultBotProperties


class BotProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_bot(self, config: Config) -> Bot:
        return Bot(
            token=config.telegram.token,
            default=DefaultBotProperties(parse_mode='HTML')
        )

    @provide(scope=Scope.APP)
    def get_dispatcher(self) -> Dispatcher:
        return Dispatcher()