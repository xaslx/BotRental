from fastapi import APIRouter, status, Response
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.application.use_cases.user.register import NewUserUseCase, RegisterUserUseCase
from src.domain.user.entity import UserEntity
from src.presentation.schemas.user import CheckCodeSchema, RegisterUserSchema, UserOutSchema
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.success import SuccessResponse
import logging
from src.presentation.controllers.handler_exception import handle_exceptions


logger = logging.getLogger(__name__)
router: APIRouter = APIRouter()


@router.post(
    '/verify-code',
    description='Эндпоинт для проверки кода',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': UserOutSchema},
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Invalid code',
        },
    },
)
@inject
@handle_exceptions
async def verify_code(
    code_schema: CheckCodeSchema,
    use_case: Depends[RegisterUserUseCase]
) -> UserOutSchema | None:

    user: UserEntity | None = await use_case.execute(schema=code_schema)
    return UserOutSchema.model_validate(user)
    


@router.post(
    '/register',
    description='Эндпоинт для регистрации нового пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': SuccessResponse},
        status.HTTP_409_CONFLICT: {
            'model': ErrorSchema,
            'description': 'User Already Exists',
        },
    },
)
@inject
@handle_exceptions
async def register_user(
    new_user: RegisterUserSchema,
    use_case: Depends[NewUserUseCase],

) -> SuccessResponse:
    
    await use_case.execute(new_user=new_user)
    return SuccessResponse(message='Код отправлен вам в Telegram')

    


# @router.post(
#     '/login',
#     description='Эндпоинт для входа',
#     status_code=status.HTTP_200_OK,
# )
# @inject
# async def login_user(
#     login_schema: LoginUserWithCode,
#     response: Response,
#     use_case: Depends[LoginUserUseCase],
# ) -> None:
    
#     token: str = await use_case.execute(telegram_id=login_schema.telegram_id, code=login_schema.confirmation_code)
#     response.set_cookie(key='user_access_token', value=token, httponly=True)


# @router.post(
#     '/logout',
#     description='Эндпоинт для выхода',
#     status_code=status.HTTP_200_OK,
# )
# @inject
# async def logout_user(
#     response: Response,
#     user: Depends[UserEntity],
# ) -> None:
    
#     response.delete_cookie(key='user_access_token')
