# Background jobs

Available with enable_jobs=true. Taskiq uses Redis Streams; the API, worker and scheduler are separate processes. ARQ is not included.

## Run the worker

```bash
sudo apt install redis-server
sudo systemctl start redis-server
redis-cli ping
```

Run these in separate terminals from the generated project:

```bash
uv run backup-service serve
```

```bash
uv run backup-service worker
```

```bash
uv run backup-service scheduler
```

## Submit and inspect work

```bash
uv run backup-service enqueue "Backup finished"
curl -fsS -X POST http://127.0.0.1:8000/jobs \
  -H 'Content-Type: application/json' \
  -d '{"message":"Index updated"}'
curl -fsS http://127.0.0.1:8000/messages/count
```

The POST returns HTTP 202 and a job ID. A successful submission is not proof of completion. The sample worker persists messages in SQLite.

## Add a job

In src/backup_service/jobs.py:

```python
from .queue import broker

@broker.task
async def refresh_index() -> str:
    # Replace with actual asynchronous application logic.
    return "refreshed"
```

Submit with `await refresh_index.kiq()`. Ensure the worker imports the module that registers the task.

The template uses a per-project stream and retains results for 24 hours. Delivery can repeat after a worker failure; make side effects idempotent. The sequential scheduler waits between submissions, does not replay missed intervals, and does not guarantee that long-running worker jobs cannot overlap.
