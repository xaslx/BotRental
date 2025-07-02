from taskiq_aio_pika import AioPikaBroker



broker: AioPikaBroker = AioPikaBroker(
    url='amqp://maksim:maksim@rabbitmq/',
)