from src.infrastructure.taskiq.broker import broker
import psutil
from aiogram import Bot
from src.const import MB
import logging
import os

token: str = os.getenv(key='TELEGRAM_TOKEN_BOT')

bot = Bot(token=token)

ADMIN_CHAT_ID: int = 340906161



@broker.task(retry=3)
async def send_notification(user_id: int, text: str) -> None:
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except Exception as e:
        pass



@broker.task(schedule=30 * 60)
async def send_system_stats() -> None:
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    msg = (
        f"🖥 <b>Мониторинг сервера</b>\n"
        f"CPU: {cpu_percent}%\n"
        f"RAM: {round(memory.used / MB, 2)} / {round(memory.total / MB, 2)} MB ({memory.percent}%)\n"
        f"Disk: {round(disk.used / MB, 2)} / {round(disk.total / MB, 2)} MB ({disk.percent}%)"
    )

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode='HTML')
