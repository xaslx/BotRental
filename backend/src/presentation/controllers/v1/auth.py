from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.application.use_cases.user.auth import SendCodeUseCase, VerifyCodeUseCase
from src.domain.user.entity import UserEntity
from src.presentation.schemas.user import CheckCodeSchema, SendCodeSchema, UserOutSchema
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.success import SuccessResponse
import logging
from src.presentation.controllers.handler_exception import handle_exceptions


logger = logging.getLogger(__name__)
router: APIRouter = APIRouter()


@router.post(
    '/send-code',
    description='Эндпоинт для отправки кода подтверждения',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': SuccessResponse},
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Invalid request',
        },
    },
)
@inject
@handle_exceptions
async def send_code(
    user_schema: SendCodeSchema,
    use_case: Depends[SendCodeUseCase],
) -> SuccessResponse:
    
    await use_case.execute(telegram_id=user_schema.telegram_id)
    return SuccessResponse(message='Код отправлен вам в Telegram')


@router.post(
    '/verify-code',
    description='Эндпоинт для проверки кода и автоматической регистрации/входа',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': UserOutSchema},
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
    use_case: Depends[VerifyCodeUseCase]
) -> UserOutSchema:
    
    user: UserEntity = await use_case.execute(schema=code_schema)
    return UserOutSchema.model_validate(user)

    


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
