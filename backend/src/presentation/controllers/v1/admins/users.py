from fastapi import APIRouter, status, HTTPException
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.domain.user.entity import UserEntity
from src.presentation.schemas.user import UserOutSchema
from src.application.use_cases.admin.users.get_users import GetAllUsersUseCase, GetUserByTelegramId
from src.presentation.decorators.check_role import check_role
from src.presentation.schemas.error import ErrorSchema


router: APIRouter = APIRouter()


@router.get(
    '/users',
    description='Эндпоинт для получения всех пользователей',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {'model': ErrorSchema, 'description': 'Permission denied.'},
    },
)
@inject
@check_role(allowed_roles=['admin'])
async def get_all_users(
    use_case: Depends[GetAllUsersUseCase],
    user: Depends[UserEntity],
) -> list[UserOutSchema] | None:
    
    users: list[UserOutSchema] = await use_case.execute()
    return users


@router.get(
    '/users/{telegram_id}',
    description='Эндпоинт для получения конкретного пользователя',
    status_code=status.HTTP_200_OK,
)
@inject
@check_role(allowed_roles=['admin'])
async def get_user_by_id(
    telegram_id: int,
    user: Depends[UserEntity],
    use_case: Depends[GetUserByTelegramId],
) -> UserOutSchema | None:
    
    return await use_case.execute(telegram_id=telegram_id)