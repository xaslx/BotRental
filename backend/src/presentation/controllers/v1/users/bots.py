from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from src.application.use_cases.user.bot.get_all_bots import GetAllBotsUseCase
from src.domain.user.entity import UserEntity
from src.presentation.schemas.bot import BotOutSchema

router: APIRouter = APIRouter()


@router.get(
    '',
    description='Эндпоинт для получения всех ботов',
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_bots(
    user: Depends[UserEntity],
    use_case: Depends[GetAllBotsUseCase],
) -> list[BotOutSchema] | None:
    res = await use_case.execute()
    return [BotOutSchema.model_validate(bot.to_dict()) for bot in res]
