"""Route application, Uvicorn and ARQ logs to one structured stderr sink."""

import logging
import sys

from loguru import logger

from .config import get_settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.bind(source=record.name).opt(exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logging() -> None:
    level = get_settings().log_level
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        serialize=True,
        enqueue=False,
        backtrace=False,
        diagnose=False,
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=level, force=True)
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "arq", "arq.worker"):
        standard_logger = logging.getLogger(name)
        standard_logger.handlers.clear()
        standard_logger.setLevel(logging.NOTSET)
        standard_logger.propagate = True
