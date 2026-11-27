# Configuration

Run commands from the project root. Settings load once per process from .env; exported environment variables take precedence. Restart the service after changes.

```dotenv
APP_HOST=127.0.0.1
APP_PORT=8123
DATABASE_PATH=data/app.sqlite3
LOG_LEVEL=INFO
```

| Setting | Default | Meaning |
| --- | --- | --- |
| APP_HOST | 127.0.0.1 | Bind address |
| APP_PORT | 8000 | HTTP port |
| DATABASE_PATH | data/app.sqlite3 | SQLite file |
| LOG_LEVEL | INFO | Log severity |
| REDIS_URL | redis://127.0.0.1:6379/0 | Jobs only |
| SCHEDULE_INTERVAL_SECONDS | 300 | Jobs only |
| NTFY_URL | Unset | Notifications only |
| NTFY_TOPIC | Unset | Notifications only |
| NTFY_TOKEN | Unset | Optional bearer token |
| NTFY_TIMEOUT_SECONDS | 5 | Notification timeout |

Override an environment setting temporarily:

```bash
APP_PORT=8123 uv run backup-service serve
```

Access validated configuration in application code:

```python
from backup_service.config import get_settings

settings = get_settings()
print(settings.database_path)
```

Keep .env out of version control. Never log Redis credentials or notification tokens. The default HTTP binding is local only. Configure authentication and TLS before exposing services remotely.

See [Diagnostics](Diagnostics) for configuration failures.
