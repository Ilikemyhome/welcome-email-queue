# Welcome Email Queue System

## Overview

This project demonstrates an event-driven architecture using React, FastAPI, RabbitMQ, and SQLite. The application accepts welcome email requests through a REST API, publishes jobs to a RabbitMQ message queue, and processes them asynchronously using a background worker.

The goal is to demonstrate asynchronous decoupling, message durability, worker resiliency, and status tracking.

---

# Architecture Topology & Data Flow

```text
+-----------------------+
|   React Frontend      |
|  (Job Submission UI)  |
+----------+------------+
           |
           | POST /api/jobs
           v
+-----------------------+
|   FastAPI Producer    |
|  Returns HTTP 202     |
+----------+------------+
           |
           | Publish Message
           v
+-----------------------+
|      RabbitMQ         |
|    Message Queue      |
+----------+------------+
           |
           | Consume Message
           v
+-----------------------+
|   Worker Consumer     |
| Processes Welcome     |
| Email Job             |
+----------+------------+
           |
           | Update Status
           v
+-----------------------+
|     SQLite Store      |
| queued -> processing  |
| -> completed          |
+-----------------------+
```

### Message Flow

1. A user submits their name and email using the React frontend.
2. The FastAPI API validates the request.
3. The API generates a unique Job ID.
4. Job status is stored as `queued`.
5. The API publishes a message to RabbitMQ.
6. The API immediately returns HTTP `202 Accepted`.
7. The worker consumes the message.
8. The worker updates the status to `processing`.
9. The worker simulates email delivery.
10. The worker updates the status to `completed`.
11. The frontend continuously polls the status endpoint and displays updates.

---

# Technology Stack

## Frontend

- React
- Vite

## Backend

- FastAPI
- Python

## Messaging Broker

- RabbitMQ

## Persistence

- SQLite

## Containerization

- Docker Compose

---

# Prerequisites & Run Guide

## Prerequisites

Install:

- Python 3.11+
- Node.js
- Docker Desktop
- UV Package Manager

---

## Start RabbitMQ

From the project root:

```bash
docker compose up -d
```

RabbitMQ Dashboard:

```text
http://localhost:15672
```

Credentials:

```text
Username: guest
Password: guest
```

---

## Start FastAPI API

From the project root:

```bash
uv run uvicorn welcome_email_queue.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Start Worker

Open a second terminal:

```bash
uv run python -m welcome_email_queue.worker
```

Expected:

```text
Worker started
```

---

## Start React Frontend

Open a third terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## Submit Sample Payload

Example request:

```json
{
  "email": "test@example.com",
  "name": "Ingrid"
}
```

Response:

```json
{
  "job_id": "123456",
  "status": "queued"
}
```

---

## Poll Job Status

```http
GET /api/jobs/{job_id}
```

Example:

```json
{
  "job_id": "123456",
  "email": "test@example.com",
  "name": "Ingrid",
  "status": "processing"
}
```

Later:

```json
{
  "job_id": "123456",
  "email": "test@example.com",
  "name": "Ingrid",
  "status": "completed"
}
```

---

# AI Disclosure & Prompt Appendix

## AI Tools Used

- Microsoft Copilot (GPT-5 based)
- ChatGPT/OpenAI

---

## Prompt Used

```text
Act as a senior distributed systems architect. Build a decoupled, event-driven service demonstrating synchronous REST ingestion and asynchronous message queue processing using FastAPI and RabbitMQ.

The project must include:

1. Ingress REST API
   - POST /api/jobs
   - GET /api/jobs/:id

2. RabbitMQ Message Broker

3. Worker Service
   - Consumes queue
   - Simulates work
   - Updates status
   - Supports ACK/NACK

4. Frontend
   - Submit jobs
   - Poll status

Provide API code, worker code, RabbitMQ configuration, and setup instructions.
```

---

## What AI Generated Correctly

The AI correctly suggested:

- FastAPI as the API framework
- RabbitMQ as the message broker
- React frontend
- Worker pattern for asynchronous processing
- Job status polling
