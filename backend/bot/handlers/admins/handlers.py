import asyncio
from aiogram import Router
from dishka.integrations.aiogram import inject, FromDishka as Depends
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter
from src.infrastructure.repositories.telegram.base import BaseTelegramRepository
from .filter import AdminProtect
from src.infrastructure.database.models.telegram_users import TelegramUser
from src.infrastructure.taskiq.tasks import send_copy_task


router: Router = Router()


@router.message(Command('notify'), StateFilter(default_state), AdminProtect())
@inject
async def notify_users(message: Message, repository: Depends[BaseTelegramRepository]):
    if not message.reply_to_message:
        await message.answer('Сделай реплай на сообщение, которое надо разослать.')
        return

    users: list[TelegramUser] = await repository.get_all_users()
    await asyncio.gather(*[
        send_copy_task.kiq(
                to_chat_id=user.telegram_id,
                from_chat_id=message.reply_to_message.chat.id,
                from_message_id=message.reply_to_message.message_id,
            ) for user in users
        ],
    )
    await message.answer('✅ Рассылка запущена.')