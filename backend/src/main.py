import logging
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI, Request
from src.domain.common.exception import DomainErrorException
from src.presentation.controllers.v1.setup_routers import setup_controllers
from contextlib import asynccontextmanager
from src.logger import setup_logger
from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as fastapi_integration
from src.config import Config
from src.ioc import AppProvider
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    logger.info('Приложение запущено')
    yield
    logger.info('Приложение выключено')


def create_app() -> FastAPI:

    config: Config = Config()
    container: AsyncContainer = make_async_container(AppProvider(), context={Config: config})

    app: FastAPI = FastAPI(title='Bot Rental', lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )
    
    setup_controllers(app=app)
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=False,
        excluded_handlers=['/metrics'],
    )
    instrumentator.instrument(app).expose(app)

    setup_controllers(app=app)
    fastapi_integration.setup_dishka(container=container, app=app)

    @app.exception_handler(DomainErrorException)
    async def domain_error_exception_handler(request: Request, exc: DomainErrorException):
        return JSONResponse(
            status_code=getattr(exc, 'status_code', exc.status_code),
            content={'detail': exc.message},
        )
    
    return app

