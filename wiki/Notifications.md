# ntfy notifications

Available with enable_ntfy=true. The service publishes to an existing ntfy instance using httpx2. No notification daemon, automatic log forwarding or public publishing route is installed.

## Configure

Set values in the private .env file:

```dotenv
NTFY_URL=https://ntfy.example.com
NTFY_TOPIC=backup-alerts
NTFY_TOKEN=tk_your_access_token
NTFY_TIMEOUT_SECONDS=5
```

Replace the example hostname and token. Subscribe to the protected topic using an ntfy client. Use HTTPS over the network.

## Publish

```bash
uv run backup-service notify "Backup completed" --title Backup --priority 3
```

From asynchronous application code:

```python
from backup_service.notifications import notify

message_id = await notify(
    "Backup completed",
    title="Backup",
    priority=4,
    tags=["white_check_mark"],
)
```

Priorities range from 1 to 5. The function returns the accepted ntfy message ID and raises on failure. No automatic retries are performed because publishing twice may duplicate notifications.

A notification outage does not make the API unready. Handle failures according to the importance of the calling operation. Do not include secrets or sensitive personal data in notifications.
