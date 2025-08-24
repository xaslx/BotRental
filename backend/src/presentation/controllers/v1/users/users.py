from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from src.application.use_cases.user.get_user_referrals import GetUserReferralsUseCase
from src.application.use_cases.user.get_user_rentals import GetUserRentalsUseCase
from src.domain.bot.entity import BotRentalEntity
from src.domain.referral.entity import ReferralEntity
from src.domain.user.entity import UserEntity
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.user import (
    BlockedUserOutSchema,
    BotRentalOutSchema,
    ReferralOutSchema,
    UserOutSchema,
)

router: APIRouter = APIRouter()


@router.get(
    '/profile',
    description='Эндпоинт для отображения профиля пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': UserOutSchema,
            'description': 'Профиль пользователя',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Пользователь не аутентифицирован',
        },
    },
)
@inject
async def get_my_profile(
    user: Depends[UserEntity],
) -> UserOutSchema | None:
    return UserOutSchema.model_validate(user.to_dict())


@router.get(
    '/profile/blocks',
    description='Эндпоинт для отображения всех блокировок пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': list[BlockedUserOutSchema],
            'description': 'Список блокировок пользователя',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Пользователь не аутентифицирован',
        },
    },
)
@inject
async def get_my_block(
    user: Depends[UserEntity],
) -> list[BlockedUserOutSchema]:
    return [BlockedUserOutSchema.model_validate(block) for block in user.blocks]


@router.get(
    '/profile/referrals',
    description='Эндпоинт для отображения всех рефералов пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': list[ReferralOutSchema],
            'description': 'Список рефералов пользователя',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Пользователь не аутентифицирован',
        },
    },
)
@inject
async def get_my_referrals(
    user: Depends[UserEntity],
    use_case: Depends[GetUserReferralsUseCase],
) -> list[ReferralOutSchema]:
    referrals: list[ReferralEntity] = await use_case.execute(referrer_id=user.id)
    return [
        ReferralOutSchema.model_validate(referral.to_dict()) for referral in referrals
    ]


@router.get(
    '/profile/rentals',
    description='Эндпоинт для отображения всех аренд ботов у пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': list[BotRentalOutSchema],
            'description': 'Список аренд пользователя',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorSchema,
            'description': 'Пользователь не аутентифицирован',
        },
    },
)
@inject
async def get_my_rentals(
    user: Depends[UserEntity],
    use_case: Depends[GetUserRentalsUseCase],
) -> list[BotRentalOutSchema]:
    rentals: list[BotRentalEntity] = await use_case.execute(user_id=user.id)
    return [BotRentalOutSchema.model_validate(rent) for rent in rentals]
