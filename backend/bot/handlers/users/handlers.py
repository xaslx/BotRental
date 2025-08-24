import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

router: Router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart(), StateFilter(default_state))
async def start_cmd(message: Message):
    await message.answer(
        text='Привет, это бот для сайта <b>BotRental</b>\n'
        'Доступные команды:\n'
        '/id - Посмотреть свой ID'
    )
    logger.info(f'Пользователь: {message.from_user.id}')


@router.message(Command('id'), StateFilter(default_state))
async def get_my_id(message: Message):
    await message.answer(
        text=f'Ваш ID: <b>{message.from_user.id}</b>\nВставьте его на сайте'
    )
    logger.info(f'Пользователь: {message.from_user.id} проверил свой ID')


@router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.answer(
        text='Доступные команды:\n /start - Запустить бота\n/id - Получить свой ID'
    )
