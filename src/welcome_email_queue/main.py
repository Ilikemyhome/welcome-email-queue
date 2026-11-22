from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import json
import aio_pika

from .rabbitmq import get_connection
from fastapi.middleware.cors import CORSMiddleware

from .database import (
    init_db,
    create_job as create_job_record,
    get_job as get_job_record
)

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


class EmailJob(BaseModel):
    email: str
    name: str


@app.post("/api/jobs", status_code=202)
async def create_job(job: EmailJob):

    job_id = str(uuid4())

    create_job_record(
        job_id,
        job.email,
        job.name
    )

    connection = await get_connection()

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(
            "welcome_emails",
            durable=True
        )

        payload = {
            "job_id": job_id,
            "email": job.email,
            "name": job.name,
        }

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=queue.name,
        )

    return {
        "job_id": job_id,
        "status": "queued",
    }


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):

    job = get_job_record(job_id)

    if not job:
        return {
            "error": "Job not found"
        }

    return {
        "job_id": job[0],
        "email": job[1],
        "name": job[2],
        "status": job[3],
    }