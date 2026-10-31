"""Environment configuration shared by API, worker and scheduler."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    host: str
    port: int
    database_path: Path
    redis_url: str
    schedule_interval_seconds: int
    log_level: str


def get_settings() -> Settings:
    """Read at call time so each process receives its own environment."""
    interval = int(os.getenv("SCHEDULE_INTERVAL_SECONDS", "300"))
    port = int(os.getenv("APP_PORT", "8000"))
    if interval < 1:
        raise ValueError("SCHEDULE_INTERVAL_SECONDS must be positive")
    if not (1 <= port <= 65535):
        raise ValueError("APP_PORT must be between 1 and 65535")
    return Settings(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=port,
        database_path=Path(os.getenv("DATABASE_PATH", "data/app.sqlite3")),
        redis_url=os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        schedule_interval_seconds=interval,
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
