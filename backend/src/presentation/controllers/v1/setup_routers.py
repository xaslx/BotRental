from fastapi import FastAPI
from src.presentation.controllers.v1.admins.bots import router as admin_bots_router
from src.presentation.controllers.v1.admins.monitoring import (
    router as admins_monitoring_router,
)
from src.presentation.controllers.v1.admins.users import router as admin_users_router
from src.presentation.controllers.v1.users.auth import router as auth_router
from src.presentation.controllers.v1.users.bots import router as bots_router
from src.presentation.controllers.v1.users.rentals import router as user_rentals
from src.presentation.controllers.v1.users.users import router as user_router


def setup_controllers(app: FastAPI):
    app.include_router(
        auth_router, prefix='/api/v1', tags=['Авторизация и Аутентификация']
    )
    app.include_router(
        admins_monitoring_router, prefix='/api/v1', tags=['Мониторинг Админ']
    )
    app.include_router(user_router, prefix='/api/v1/users', tags=['Пользователи'])
    app.include_router(
        admin_users_router, prefix='/api/v1/users', tags=['Пользователи Админ']
    )
    app.include_router(admin_bots_router, prefix='/api/v1/bots', tags=['Боты Админ'])
    app.include_router(bots_router, prefix='/api/v1/bots', tags=['Боты'])
    app.include_router(user_rentals, prefix='/api/v1/rentals', tags=['Аренды'])
