# Ubuntu deployment

Install the generated project as a non-root user on an Ubuntu systemd host. Use a project path without whitespace. Install uv and Task for that user.

```bash
cd ~/projects/backup-service
task setup
cp .env.example .env
uv run backup-service init-db
task doctor
sudo bash deploy/install.sh
```

Review .env first. Install and start Redis if jobs are enabled. The installer creates and starts the API unit and, when enabled, worker and scheduler units.

## Operate

```bash
systemctl status backup-service-api.service
sudo journalctl -fu backup-service-api.service
task doctor -- --require-running
```

For jobs:

```bash
systemctl status backup-service-worker.service
systemctl status backup-service-scheduler.service
sudo journalctl -u backup-service-worker.service -n 50
```

## Update

Back up persistent data before changing code or schema. As the service user, update the project and install its committed lockfile:

```bash
uv sync --frozen --no-dev
sudo systemctl restart backup-service-api.service
```

Restart worker and scheduler too if enabled. Verify readiness:

```bash
curl -fsS http://127.0.0.1:8000/health/ready
task doctor -- --require-running
```

Systemd supervises foreground processes. Application logs are routed to stderr as structured JSON. The installer does not configure reverse proxies, TLS, backups, migrations or remote authentication.
