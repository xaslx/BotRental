import aiormq
import json
from src.config import Config

config: Config = Config()


async def publish(chat_id: str, text: str):

    connection = await aiormq.connect(
        f'amqp://{config.rabbitmq.user}:{config.rabbitmq.password}@rabbitmq/'
    )
    channel = await connection.channel()

    await channel.exchange_declare('main_exchange', exchange_type='direct')

    telegram_data = {
        'chat_id': chat_id,
        'text': text
    }

    await channel.basic_publish(
        body=json.dumps(telegram_data).encode('utf-8'),
        exchange='main_exchange',
        routing_key='main_routing_key'
    )

    await connection.close()