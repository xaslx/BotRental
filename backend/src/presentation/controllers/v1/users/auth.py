import logging

from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import Response
from src.application.use_cases.user.auth import (RefreshTokenUseCase,
                                                 SendCodeUseCase,
                                                 VerifyCodeUseCase)
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.success import SuccessResponse
from src.presentation.schemas.user import (CheckCodeSchema, SendCodeSchema,
                                           UserOutSchema)


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
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'model': ErrorSchema,
            'description': 'Please wait 5 minutes before requesting a new code',
        },
    },
)
@inject
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
async def verify_code(
    code_schema: CheckCodeSchema,
    use_case: Depends[VerifyCodeUseCase],
    response: Response,
) -> UserOutSchema:
    
    user, access_token, refresh_token = await use_case.execute(schema=code_schema)

    response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=900)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=1296000)
    return UserOutSchema.model_validate(user)

    
@router.post(
    '/refresh-token',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для обновления access token',
    responses={
        status.HTTP_200_OK: {
            'model': SuccessResponse,
            'description': 'Access token успешно обновлён',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Refresh token отсутствует или недействителен',
        },
    },

)
@inject
async def refresh_token(
    response: Response,
    request: Request,
    use_case: Depends[RefreshTokenUseCase],
) -> SuccessResponse:
    
    token: str | None = request.cookies.get('refresh_token')
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token not found')

    new_access_token: str = await use_case.execute(refresh_token=token)
    response.set_cookie(key='access_token', value=new_access_token, httponly=True, max_age=900)
    return SuccessResponse(message='Access token успешно обновлён')




@router.post(
    '/logout',
    description='Эндпоинт для выхода пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': SuccessResponse,
            'description': 'Куки токенов удалены, пользователь вышел из системы',
        },
    },
)
async def logout_user(response: Response) -> SuccessResponse:

    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')
    return SuccessResponse(message='Вы успешно вышли из системы')

