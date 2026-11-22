import aio_pika

RABBITMQ_URL = "amqp://guest:guest@localhost/"


async def get_connection():
    return await aio_pika.connect_robust(
        RABBITMQ_URL
    )