import asyncio
import json

from .rabbitmq import get_connection
from .database import update_status

async def process_message(message):

    try:

        data = json.loads(
            message.body.decode()
        )

        job_id = data["job_id"]

        print(f"Processing {job_id}")

        update_status(
            job_id,
            "processing"
        )

        await asyncio.sleep(20)

        update_status(
            job_id,
            "completed"
        )

        print(
            f"Welcome email sent to "
            f"{data['email']}"
        )

        await message.ack()

        print(
            f"ACK sent for {job_id}"
        )

    except Exception as e:

        print(
            f"Error processing message: {e}"
        )

        await message.nack(
            requeue=True
        )

        print(
            f"NACK sent for {job_id}"
        )
async def main():

    connection = await get_connection()

    channel = await connection.channel()

    queue = await channel.declare_queue(
        "welcome_emails",
        durable=True
    )

    await queue.consume(
        process_message
    )

    print("Worker started")

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())