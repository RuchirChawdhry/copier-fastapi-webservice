# FastAPI Webservice Copier Template

Generate backend-only Python services for Ubuntu, with FastAPI, uv, SQLite and systemd. Select Taskiq, FastMCP and ntfy independently at generation time.

## Highlights

- **Ready to run**: Typed REST endpoints, health checks, SQLite and an installed CLI.
- **Optional background jobs**: Redis Streams, Taskiq worker and a separate periodic scheduler.
- **Agent-ready MCP**: Standalone FastMCP on the existing HTTP server.
- **Push notifications**: Publish application events to a configured ntfy instance.
- **Fast feedback**: Ruff, ty, pytest, benchmarks and machine-readable diagnostics.
- **Repeatable deployment**: Shared CI, systemd units, cached configuration and gzip compression.

## Quick start

```bash
uvx copier copy --vcs-ref HEAD gh:RuchirChawdhry/copier-fastapi-webservice backup-service
cd backup-service
git init -b main
task setup
cp .env.example .env
uv run backup-service init-db
uv run backup-service serve
```

Choose no when asked about jobs if Redis is not required. For a job-enabled service, install and start Redis first.

Open [FastAPI interactive docs](http://127.0.0.1:8000/docs) locally, or run `curl http://127.0.0.1:8000/health/ready`.

## Guides

- [Getting Started](Getting-Started) — feature selection and first run.
- [Configuration](Configuration) — environment settings and secrets.
- [HTTP API](HTTP-API) — requests, health and compression.
- [Background Jobs](Background-Jobs) — submit work and run the scheduler.
- [MCP](MCP) — register tools and connect agents.
- [Notifications](Notifications) — send ntfy messages.
- [Deployment](Deployment) — install and operate Ubuntu services.
- [Development and CI](Development-and-CI) — checks and benchmarks.
- [Diagnostics](Diagnostics) — diagnose failures with JSON.

[Source repository](https://github.com/RuchirChawdhry/copier-fastapi-webservice) · [Actions](https://github.com/RuchirChawdhry/copier-fastapi-webservice/actions)
