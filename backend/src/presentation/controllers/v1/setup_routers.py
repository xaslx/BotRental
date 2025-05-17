from fastapi import FastAPI
from src.presentation.controllers.v1.main import router as main_router



def setup_controllers(app: FastAPI):

    app.include_router(main_router, tags=['Главная страница'])