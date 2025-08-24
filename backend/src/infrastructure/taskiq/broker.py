from taskiq_aio_pika import AioPikaBroker

broker: AioPikaBroker = AioPikaBroker(
    url='amqp://maksim:maksim@rabbitmq/',
    queue_name='notifications_queue',
    declare_queues=True,
    declare_queues_kwargs={
        'durable': True,
    },
)
