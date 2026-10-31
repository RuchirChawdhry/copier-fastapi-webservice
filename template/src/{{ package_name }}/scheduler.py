"""One dedicated scheduler process enqueues jobs. Never start in an API worker."""

import asyncio
from collections.abc import Callable

import schedule
from loguru import logger

from .config import get_settings
from .queue import new_pool


def build_scheduler(callback: Callable[[], None], interval_seconds: int) -> schedule.Scheduler:
    scheduler = schedule.Scheduler()
    scheduler.every(interval_seconds).seconds.do(callback)
    return scheduler


async def run_scheduler() -> None:
    """Run the in-memory schedule only within its own systemd process."""
    settings = get_settings()
    redis = await new_pool()

    async def submit_heartbeat() -> None:
        try:
            job = await redis.enqueue_job("save_message", "scheduled heartbeat")
            logger.info("Enqueued scheduled job {}", getattr(job, "job_id", None))
        except Exception:
            logger.exception("Unable to enqueue scheduled job")

    pending: set[asyncio.Task] = set()

    def dispatch() -> None:
        task = asyncio.create_task(submit_heartbeat())
        pending.add(task)
        task.add_done_callback(pending.discard)

    scheduler = build_scheduler(dispatch, settings.schedule_interval_seconds)
    logger.info("Scheduler active: interval={}s", settings.schedule_interval_seconds)
    try:
        while True:
            scheduler.run_pending()
            await asyncio.sleep(1)
    finally:
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        await redis.aclose()
