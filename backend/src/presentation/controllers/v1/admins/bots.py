from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.presentation.schemas.error import ErrorSchema
from src.domain.bot.entity import BotEntity
from src.presentation.schemas.bot import BotOutSchema, CreateBotSchema
from src.application.use_cases.admin.bot.create_bot import CreateNewBotUseCase
from src.domain.user.entity import UserEntity
from src.presentation.decorators.check_role import check_role



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
    return BotOutSchema.model_validate(bot)