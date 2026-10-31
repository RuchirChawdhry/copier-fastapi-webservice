"""Structured logs go to stderr, where systemd's journal collects them."""

import sys

from loguru import logger

from .config import get_settings


def configure_logging() -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level=get_settings().log_level.upper(),
        serialize=True,
        enqueue=False,
        backtrace=False,
        diagnose=False,
    )
