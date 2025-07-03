from src.infrastructure.taskiq.broker import broker
import psutil
from aiogram import Bot
from src.const import MB
import os
import logging

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



@broker.task(retry=3)
async def send_notification(user_id: int, text: str) -> None:
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except Exception as e:
        logger.error(f'Ошибка в send_notification для user_id={user_id}: {e}', exc_info=True)


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