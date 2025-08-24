from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from src.application.use_cases.admin.bot.change_status_bot import (
    ActivateBotUseCase,
    DeactivateBotUseCase,
)
from src.application.use_cases.admin.bot.create_bot import CreateNewBotUseCase
from src.application.use_cases.admin.bot.delete_bot import DeleteBotUseCase
from src.application.use_cases.admin.bot.get_all_bots_with_rentals import (
    GetAllBotsWithRentalsUseCase,
)
from src.application.use_cases.admin.bot.update_bot import UpdateBotUseCase
from src.domain.bot.entity import BotEntity
from src.domain.user.entity import UserEntity
from src.presentation.decorators.check_role import check_role
from src.presentation.schemas.bot import (
    BotAdminOutSchema,
    BotOutSchema,
    CreateBotSchema,
    UpdateBotSchema,
)
from src.presentation.schemas.error import ErrorSchema

router: APIRouter = APIRouter()


@router.post(
    '',
    description='Эндпоинт для добавления новых ботов',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Bot successfully created',
            'model': BotOutSchema,
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Validation error (e.g., invalid price or empty fields)',
            'model': ErrorSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def create_bot(
    new_bot: CreateBotSchema,
    user: Depends[UserEntity],
    use_case: Depends[CreateNewBotUseCase],
) -> BotOutSchema:
    bot: BotEntity = await use_case.execute(bot=new_bot, admin=user)
    return BotOutSchema.model_validate(bot.to_dict())


@router.get(
    '/rentals',
    description='Эндпоинт для получения арендодателей бота',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': list[BotAdminOutSchema]},
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def get_all_bots_with_rentals(
    user: Depends[UserEntity],
    use_case: Depends[GetAllBotsWithRentalsUseCase],
) -> list[BotAdminOutSchema] | None:
    result: list[BotEntity] | None = await use_case.execute()
    return [BotAdminOutSchema.model_validate(bot.to_dict()) for bot in result]


@router.patch(
    '/{bot_id}',
    description='Эндпоинт для обновления бота',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BotAdminOutSchema,
            'description': 'Bot successfully updated.',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action.',
            'model': ErrorSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Bot not found.',
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def update_bot(
    bot_id: int,
    update_schema: UpdateBotSchema,
    user: Depends[UserEntity],
    use_case: Depends[UpdateBotUseCase],
) -> BotAdminOutSchema:
    updated_bot: BotEntity = await use_case.execute(
        bot_id=bot_id, admin=user, update_schema=update_schema
    )
    return BotAdminOutSchema.model_validate(updated_bot.to_dict())


@router.delete(
    '/{bot_id}',
    description='Эндпоинт для удаления бота',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Bot successfully deleted.'},
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Bot not found.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Bot has already been deleted.',
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def delete_bot(
    bot_id: int,
    user: Depends[UserEntity],
    use_case: Depends[DeleteBotUseCase],
) -> None:
    await use_case.execute(bot_id=bot_id, admin=user)


@router.post(
    '/{bot_id}/activate',
    description='Эндпоинт для активации бота',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BotAdminOutSchema,
            'description': 'Bot successfully updated.',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action.',
            'model': ErrorSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Bot not found.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Bot already activated.',
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def activate_bot(
    bot_id: int,
    user: Depends[UserEntity],
    use_case: Depends[ActivateBotUseCase],
) -> BotAdminOutSchema:
    bot: BotEntity = await use_case.execute(bot_id=bot_id, admin=user)
    return BotAdminOutSchema.model_validate(bot.to_dict())


@router.post(
    '/{bot_id}/deactivate',
    description='Эндпоинт для активации бота',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BotAdminOutSchema,
            'description': 'Bot successfully updated.',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action.',
            'model': ErrorSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'Bot not found.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Bot already deactivated.',
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def deactivate_bot(
    bot_id: int,
    user: Depends[UserEntity],
    use_case: Depends[DeactivateBotUseCase],
) -> BotAdminOutSchema:
    bot: BotEntity = await use_case.execute(bot_id=bot_id, admin=user)
    return BotAdminOutSchema.model_validate(bot.to_dict())
