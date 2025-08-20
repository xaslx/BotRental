from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.presentation.schemas.error import ErrorSchema
from src.domain.bot.entity import BotRentalEntity
from src.application.use_cases.user.bot.rent_bot import RentBotUseCase
from src.presentation.schemas.bot import BotRentalOutSchema, CreateBotRentSchema
from src.domain.user.entity import UserEntity



router: APIRouter = APIRouter()


@router.post(
    '/{bot_id}',
    description='Эндпоинт для аренды бота',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BotRentalOutSchema},
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': (
                'Бота нельзя арендовать или аренда некорректна. '
            ),
        },
        status.HTTP_402_PAYMENT_REQUIRED: {
            'model': ErrorSchema,
            'description': 'Недостаточно средств для аренды.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Бот не найден.',
        },
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorSchema, 'description': 'Пользователь не аутентифицирован'},
    },
)
@inject
async def rent_bot(
    bot_id: int,
    new_rent: CreateBotRentSchema,
    user: Depends[UserEntity],
    use_case: Depends[RentBotUseCase],
) -> BotRentalOutSchema:
    
    res: BotRentalEntity = await use_case.execute(bot_id=bot_id, user=user, schema=new_rent)
    return BotRentalOutSchema.model_validate(res)



@router.post(
    '{bot_id}/stop',
    description='Эндпоинт для остановки аренды',
    status_code=status.HTTP_200_OK,
)
@inject
async def stop_active_rental():
    ...



@router.post(
    '{bot_id}/start',
    description='Эндпоинт для продолжения аренды',
    status_code=status.HTTP_200_OK,
)
@inject
async def start_active_rental():
    ...
    