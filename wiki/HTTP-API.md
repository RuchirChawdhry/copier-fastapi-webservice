# HTTP API

The service exposes typed FastAPI endpoints. Visit /docs for interactive OpenAPI and /openapi.json for the schema.

```bash
curl -fsS http://127.0.0.1:8000/health/live
curl -fsS http://127.0.0.1:8000/health/ready
curl -fsS http://127.0.0.1:8000/messages/count
```

| Endpoint | Purpose |
| --- | --- |
| GET /health/live | Process liveness |
| GET /health or /health/ready | SQLite and optional Redis readiness |
| GET /messages/count | Persisted message count |
| POST /jobs | Submit a job, when enabled |

Readiness returns HTTP 503 on dependency failure. Liveness does not depend on Redis.

## Add a route

Add a typed route to the router in src/backup_service/api.py:

```python
from pydantic import BaseModel

class BackupStatus(BaseModel):
    completed: bool

@router.get("/backup/status")
async def backup_status() -> BackupStatus:
    return BackupStatus(completed=True)
```

Move real business logic out of the HTTP adapter; reuse it from CLI or MCP tools.

## Compression

Built-in GZip middleware uses a 1024-byte minimum for ordinary responses and compression level 5. Clients negotiate gzip; SSE is excluded.

```bash
curl --compressed -D - -o /dev/null http://127.0.0.1:8000/openapi.json
curl -H 'Accept-Encoding: identity' -D - -o /dev/null http://127.0.0.1:8000/openapi.json
```

Check Content-Encoding and Vary. Small health responses are not compressed. Do not enable compression on sensitive reflected responses without reviewing security implications.
