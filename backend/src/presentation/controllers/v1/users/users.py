from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.user import UserOutSchema
from src.domain.user.entity import UserEntity


router: APIRouter = APIRouter()


@router.get(
    '/me',
    description='Эндпоинт для отображения профиля пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': UserOutSchema, 'description': 'Профиль пользователя'},
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorSchema, 'description': 'Пользователь не аутентифицирован'},
    }
)
@inject
async def get_my_profile(
    user: Depends[UserEntity],
) -> UserOutSchema | None:
    
    return UserOutSchema.model_validate(user.to_dict())