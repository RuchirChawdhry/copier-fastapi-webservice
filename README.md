# Copier FastAPI Webservice

Backend-only Copier template for long-running Ubuntu services with FastAPI, SQLite,
Cyclopts, Rich, Loguru, uv and systemd. Redis and ARQ jobs are optional at generation time.

```bash
uvx --from copier copier copy gh:RuchirChawdhry/copier-fastapi-webservice my-service
cd my-service
uv sync
cp .env.example .env
uv run my-service init-db
uv run my-service serve
```

Set `enable_jobs=false` to omit Redis, ARQ, queue and scheduler modules, job commands,
job routes, configuration, tests and service units. The default preserves the original
three-process architecture. ARQ is in maintenance-only mode; see its upstream README.

```bash
uvx --from copier copier copy --defaults --data enable_jobs=false gh:RuchirChawdhry/copier-fastapi-webservice my-service
```

The generated `.python-version` is the authoritative interpreter pin. All processes
read project-root .env through cached validated settings; environment variables win.
Template CI uses the shared Copier workflow, and generated-project CI remains PR-only.

## Template tests

```bash
uv run --no-project --with copier --with pytest pytest tests -q
```
