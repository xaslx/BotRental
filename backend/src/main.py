import logging
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from src.presentation.controllers.v1.setup_routers import setup_controllers
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield



def create_app() -> FastAPI:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    app: FastAPI = FastAPI(title='Bot Rental')
    setup_controllers(app=app)
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=False,
        excluded_handlers=["/metrics"],
    )
    instrumentator.instrument(app).expose(app)
    
    return app

