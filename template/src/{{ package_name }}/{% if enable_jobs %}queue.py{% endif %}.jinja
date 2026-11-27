"""ARQ connection helpers. Redis is for jobs, not SQLite persistence."""

import orjson
from arq import create_pool
from arq.connections import RedisSettings

from .config import get_settings


def redis_settings() -> RedisSettings:
    return RedisSettings.from_dsn(get_settings().redis_url)


async def new_pool():
    return await create_pool(
        redis_settings(),
        job_serializer=orjson.dumps,
        job_deserializer=orjson.loads,
    )
