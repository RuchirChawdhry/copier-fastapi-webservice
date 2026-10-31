"""Background jobs must remain independent of HTTP request lifecycles."""

import asyncio

from loguru import logger

from .db import record_message


async def save_message(ctx: dict, message: str) -> int:
    """Example task: safely write one message to SQLite."""
    message_id = await asyncio.to_thread(record_message, message)
    logger.info("Saved job message id={}", message_id)
    return message_id
