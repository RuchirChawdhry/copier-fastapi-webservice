"""Exercise the installed wheel and real SQLite persistence."""

import os
import sqlite3
import subprocess
from contextlib import closing


def test_installed_cli_initializes_sqlite(tmp_path):
    database = tmp_path / "nested" / "app.sqlite3"
    env = {**os.environ, "DATABASE_PATH": str(database)}
    command = [os.environ["CLI_EXECUTABLE"], "init-db"]
    for _ in range(2):
        result = subprocess.run(
            command, env=env, capture_output=True, text=True, timeout=15
        )
        assert result.returncode == 0, result.stderr
        assert "SQLite initialized" in result.stdout
    assert database.is_file()
    with closing(sqlite3.connect(database)) as connection:
        assert connection.execute("SELECT count(*) FROM messages").fetchone() == (0,)
        columns = connection.execute("PRAGMA table_info(messages)").fetchall()
        assert [column[1] for column in columns] == ["id", "message", "created_at"]
