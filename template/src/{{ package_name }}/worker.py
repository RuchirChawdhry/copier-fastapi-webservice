"""ARQ worker process configuration, invoked by the Cyclopts CLI."""

import asyncio

import orjson

from .db import init_db
from .jobs import save_message
from .queue import redis_settings


async def on_startup(ctx: dict) -> None:
    await asyncio.to_thread(init_db)


class WorkerSettings:
    functions = [save_message]
    on_startup = on_startup
    redis_settings = redis_settings()
    job_serializer = orjson.dumps
    job_deserializer = orjson.loads
    max_jobs = 10
    job_timeout = 300
