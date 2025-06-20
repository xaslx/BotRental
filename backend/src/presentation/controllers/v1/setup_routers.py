from fastapi import FastAPI
from src.presentation.controllers.v1.users.auth import router as auth_router
from src.presentation.controllers.v1.admins.monitoring import router as admins_monitoring_router
from src.presentation.controllers.v1.users.users import router as user_router
from src.presentation.controllers.v1.admins.users import router as admins_users_router


def setup_controllers(app: FastAPI):


    app.include_router(auth_router, prefix='/api/v1', tags=['Авторизация и Аутентификация'])
    app.include_router(admins_monitoring_router, prefix='/api/v1/admins', tags=['Мониторинг Админ'])
    app.include_router(user_router, prefix='/api/v1/users', tags=['Пользователи'])
    app.include_router(admins_users_router, prefix='/api/v1/admins', tags=['Пользователи Админ'])