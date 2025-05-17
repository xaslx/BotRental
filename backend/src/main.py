import logging
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from src.presentation.controllers.v1.setup_routers import setup_controllers
from contextlib import asynccontextmanager
from src.logger import setup_logger


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    logger.info('Приложение запущено')
    yield
    logger.info('Приложение выключено')


def create_app() -> FastAPI:


    app: FastAPI = FastAPI(title='Bot Rental', lifespan=lifespan)
    setup_controllers(app=app)
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=False,
        excluded_handlers=["/metrics"],
    )
    instrumentator.instrument(app).expose(app)
    
    return app

