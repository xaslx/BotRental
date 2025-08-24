from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from src.application.use_cases.user.bot.rent_bot import RentBotUseCase
from src.application.use_cases.user.bot.start_bot import StartBotRentalUseCase
from src.application.use_cases.user.bot.stop_bot import StopBotRentalUseCase
from src.domain.bot.entity import BotRentalEntity
from src.domain.user.entity import UserEntity
from src.presentation.schemas.bot import BotRentalOutSchema, CreateBotRentSchema
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.success import SuccessResponse

router: APIRouter = APIRouter()


@router.post(
    '/{bot_id}',
    description='Эндпоинт для аренды бота',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BotRentalOutSchema},
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': ('Бота нельзя арендовать или аренда некорректна. '),
        },
        status.HTTP_402_PAYMENT_REQUIRED: {
            'model': ErrorSchema,
            'description': 'Недостаточно средств для аренды.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Бот не найден.',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Пользователь не аутентифицирован',
        },
    },
)
@inject
async def rent_bot(
    bot_id: int,
    new_rent: CreateBotRentSchema,
    user: Depends[UserEntity],
    use_case: Depends[RentBotUseCase],
) -> BotRentalOutSchema:
    res: BotRentalEntity = await use_case.execute(
        bot_id=bot_id, user=user, schema=new_rent
    )
    return BotRentalOutSchema.model_validate(res)


@router.post(
    '/{rental_id}/stop',
    description='Эндпоинт для остановки аренды',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': SuccessResponse},
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Пользователь не аутентифицирован',
        },
        status.HTTP_403_FORBIDDEN: {
            'model': ErrorSchema,
            'description': 'Недостаточно прав',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Аренда не найдена',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Аренда уже остановлена.',
        },
    },
)
@inject
async def stop_active_rental(
    rental_id: int,
    user: Depends[UserEntity],
    use_case: Depends[StopBotRentalUseCase],
) -> SuccessResponse:
    await use_case.execute(rental_id=rental_id, user=user)
    return SuccessResponse(message='Аренда бота остановлена.')


@router.post(
    '{rental_id}/start',
    description='Эндпоинт для продолжения аренды',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': SuccessResponse},
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Пользователь не аутентифицирован',
        },
        status.HTTP_403_FORBIDDEN: {
            'model': ErrorSchema,
            'description': 'Недостаточно прав',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Аренда не найдена',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Аренда уже активна.',
        },
    },
)
@inject
async def start_active_rental(
    rental_id: int,
    user: Depends[UserEntity],
    use_case: Depends[StartBotRentalUseCase],
) -> SuccessResponse:
    await use_case.execute(rental_id=rental_id, user=user)
    return SuccessResponse(message='Аренда бота включена.')
