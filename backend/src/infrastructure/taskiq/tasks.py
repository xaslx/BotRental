import asyncio
import logging
import os

import psutil
from aiogram import Bot
from src.const import MB
from src.infrastructure.taskiq.broker import broker

token: str = os.getenv(key='TELEGRAM_TOKEN_BOT')

bot: Bot = Bot(token=token)

ADMIN_CHAT_ID: int = 340906161


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


log_file_path = os.path.join(os.path.dirname(__file__), 'error.log')

file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


@broker.task
async def send_notification(user_id: int, text: str) -> None:
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except Exception as e:
        logger.error(
            f'Ошибка в send_notification для user_id={user_id}: {e}', exc_info=True
        )


@broker.task
async def send_notification_for_admin(text: str) -> None:
    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    except Exception as e:
        logger.error(
            f'Ошибка в send_notification для user_id={ADMIN_CHAT_ID}: {e}',
            exc_info=True,
        )


@broker.task(schedule=[{'cron': '*/10 * * * *'}])
async def send_system_stats() -> None:
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        memory_total_mb = round(memory.total / MB, 2)
        memory_used_mb = round(memory.used / MB, 2)
        memory_percent = memory.percent

        disk_total_mb = round(disk.total / MB, 2)
        disk_used_mb = round(disk.used / MB, 2)
        disk_percent = disk.percent

        msg = (
            f'🖥 <b>Мониторинг сервера</b>\n'
            f'🧠 CPU: {cpu_percent}%\n\n'
            f'💾 Память:\n'
            f'• Всего: {memory_total_mb} MB\n'
            f'• Использовано: {memory_used_mb} MB\n'
            f'• Загрузка: {memory_percent}%\n\n'
            f'📀 Диск:\n'
            f'• Всего: {disk_total_mb} MB\n'
            f'• Использовано: {disk_used_mb} MB\n'
            f'• Загрузка: {disk_percent}%'
        )

        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode='HTML')

    except Exception as e:
        logger.error(f'Ошибка в send_system_stats: {e}', exc_info=True)


@broker.task
async def send_copy_task(to_chat_id: int, from_chat_id: int, from_message_id: int):
    try:
        await bot.copy_message(
            chat_id=to_chat_id, from_chat_id=from_chat_id, message_id=from_message_id
        )
        await asyncio.sleep(0.4)
    except Exception as e:
        print(f'Ошибка рассылки пользователю {to_chat_id}: {e}')
        raise e
