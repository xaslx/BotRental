from fastapi import FastAPI
from src.presentation.controllers.v1.auth import router as auth_router
from src.presentation.controllers.v1.monitoring import router as monitoring_router
from src.presentation.controllers.v1.user import router as user_router



def setup_controllers(app: FastAPI):


    app.include_router(auth_router, prefix='/api/v1', tags=['Авторизация и Аутентификация'])
    app.include_router(monitoring_router, prefix='/api/v1', tags=['Мониторинг'])
    app.include_router(user_router, prefix='/api/v1/users', tags=['Пользователи'])