# Diagnostics and troubleshooting

Run from the generated project root after task setup:

```bash
task doctor
task doctor -- --require-running
uv run --no-sync backup-service doctor | jq '.checks[] | select(.status == "fail")'
```

The report contains schema_version, overall status and a list of checks. Each check has an id, status, detail and suggested action. Failures return exit code 1; warnings alone return 0.

Illustrative failure:

```json
{
  "id": "redis",
  "status": "fail",
  "detail": "Redis ping failed.",
  "action": "Check REDIS_URL, Redis service status and credentials."
}
```

Checks cover the Python pin, direct dependency requirements, settings, SQLite, TCP endpoint, HTTP readiness, systemd and optional Redis or ntfy configuration. A stopped API is a warning unless require-running is selected. Doctor does not repair services, install dependencies or send notifications.

| Symptom | Action |
| --- | --- |
| Invalid settings | Review .env; exported variables override it |
| Missing database | Run init-db for a new database; inspect permissions for existing data |
| Redis unavailable | Run redis-cli ping and inspect Redis logs |
| Port not listening | Start the API; inspect systemd logs |
| HTTP 503 | Check dependency readiness and service logs |
| MCP 421 or 403 | Use loopback URL and trusted Host/Origin; do not disable protection |
| ntfy publishing fails | Verify server URL, topic, access token and network |
| Hooks absent | Initialize Git, then run task setup |

Useful local commands:

```bash
curl -i http://127.0.0.1:8000/health/ready
sudo journalctl -u backup-service-api.service -n 50 --no-pager
task resources
```

Doctor does not verify transitive requirements, live ntfy delivery or the process identity behind a port. It requires an installed project environment.
