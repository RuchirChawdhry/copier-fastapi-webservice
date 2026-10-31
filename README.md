# Copier FastAPI Webservice

A backend-only, batteries-included [Copier](https://copier.readthedocs.io/) template for Ubuntu services that survive reboots.

**Generated projects include:** FastAPI, uvicorn, SQLite (WAL), Redis-backed ARQ workers, an independent `schedule` dispatcher, orjson responses, Loguru, a Cyclopts + Rich CLI, Ruff, pytest, uv + Python 3.14.7, and systemd auto-start installers. No frontend, containers or UI files.

## Generate a project

```bash
uvx --from copier copier copy gh:RuchirChawdhry/copier-fastapi-webservice my-service
cd my-service
uv sync
cp .env.example .env
uv run my-service init-db
```

Use your chosen `cli_command` in place of `my-service`.

## Why three services?

- **API:** serves HTTP requests on `127.0.0.1:8000` by default.
- **Worker:** consumes jobs from Redis using ARQ.
- **Scheduler:** runs the lightweight `schedule` dispatcher and enqueues work into Redis.

Each has its own `systemd` service, with `Restart=always` and `WantedBy=multi-user.target`. Run `sudo ./deploy/install.sh` from a generated project to enable them at boot. The installer never modifies the template repository.

## Template policy

The template repository intentionally has **no** root `.github/workflows`: GitHub Actions are inert here. Generated projects get a PR-only workflow that calls `RuchirChawdhry/ci-workflows` for Python CLI checks and distribution builds. No push, schedule or workflow_dispatch trigger.

The `celer` package is a machine-learning Lasso optimizer, not a task runner. This template uses ARQ for jobs, and does not include Celery alongside it unless a distinct Celery backend is deliberately added later.

## Test the template

```bash
uv run --no-project --with copier --with pytest pytest tests -q
```

Generated projects also include their own runnable tests and `AGENTS.md` with test-first development guidance. Python 3.14.7 is used for generated projects. Run the Copier contract tests with any compatible local Python/Copier interpreter.
