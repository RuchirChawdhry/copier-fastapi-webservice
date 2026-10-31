"""Small SQLite persistence layer: short transactions and WAL."""

import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from .config import get_settings


def _database_path(path: Path | None) -> Path:
    return path if path is not None else get_settings().database_path


def _connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.execute("PRAGMA busy_timeout=10000")
    connection.execute("PRAGMA journal_mode=WAL")
    return connection


def init_db(path: Path | None = None) -> None:
    """Create schema without introducing a heavyweight ORM."""
    with closing(_connect(_database_path(path))) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def record_message(message: str, path: Path | None = None) -> int:
    """Persist a background-job result atomically."""
    with closing(_connect(_database_path(path))) as connection, connection:
        cursor = connection.execute(
            "INSERT INTO messages (message, created_at) VALUES (?, ?)",
            (message, datetime.now(UTC).isoformat()),
        )
        assert cursor.lastrowid is not None
        return cursor.lastrowid


def count_messages(path: Path | None = None) -> int:
    with closing(_connect(_database_path(path))) as connection:
        row = connection.execute("SELECT count(*) FROM messages").fetchone()
        assert row is not None
        return int(row[0])
