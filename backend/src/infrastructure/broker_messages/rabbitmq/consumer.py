import asyncio
import aiormq
import json
from aiormq.abc import DeliveredMessage
from backend.src.config import Config
import logging
import aiohttp


config: Config = Config()
logger = logging.getLogger(__name__)


async def send_telegram_message(chat_id: str, text: str):
    bot_token: str = config.telegram.token
    url: str = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    payload: dict[str, str] = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                response_text = await response.text()
                logger.error(f'Ошибка при отправке в Telegram: {response.status}, {response_text}')
            else:
                logger.info(f'Сообщение отправлено в Telegram чат {chat_id}')


async def on_message(message: DeliveredMessage):
    try:
        telegram_data = json.loads(message.body.decode('utf-8'))
        logger.info(f'Получены данные для отправки в Telegram: {telegram_data}')

        await send_telegram_message(
            chat_id=telegram_data['chat_id'],
            text=telegram_data['text']
        )

        await message.channel.basic_ack(delivery_tag=message.delivery.delivery_tag)
    except Exception as e:
        logger.error(f'Ошибка при обработке сообщения: {e}')


async def main():
    connection = await aiormq.connect(
        f'amqp://{config.rabbitmq.user}:{config.rabbitmq.password}@rabbitmq/'
    )
    channel = await connection.channel()

    await channel.exchange_declare('main_exchange', exchange_type='direct')
    declare_ok = await channel.queue_declare('telegram_queue')
    await channel.queue_bind(
        queue=declare_ok.queue,
        exchange='main_exchange',
        routing_key='main_routing_key'
    )

    await channel.basic_qos(prefetch_count=1)
    await channel.basic_consume(declare_ok.queue, on_message, no_ack=False)

    logger.info('Ожидание сообщений для Telegram...')
    await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())