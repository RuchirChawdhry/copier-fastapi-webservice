# Getting started

Install [uv](https://docs.astral.sh/uv/) and [Task](https://taskfile.dev/). Git is recommended. The generated .python-version selects Python; uv manages the environment.

## Choose a profile

| Flag | Default | Includes |
| --- | --- | --- |
| enable_jobs | true | Redis, Taskiq, scheduler |
| enable_mcp | false | FastMCP server |
| enable_ntfy | false | Outbound push notifications |

Minimal HTTP service:

```bash
uvx copier copy --vcs-ref HEAD --defaults \
  --data 'project_name=Backup Service' \
  --data enable_jobs=false \
  gh:RuchirChawdhry/copier-fastapi-webservice backup-service
```

Agent-facing service without Redis:

```bash
uvx copier copy --vcs-ref HEAD --defaults \
  --data 'project_name=Backup Service' \
  --data enable_jobs=false --data enable_mcp=true \
  gh:RuchirChawdhry/copier-fastapi-webservice backup-service
```

All features:

```bash
uvx copier copy --vcs-ref HEAD --defaults \
  --data 'project_name=Backup Service' \
  --data enable_jobs=true --data enable_mcp=true --data enable_ntfy=true \
  gh:RuchirChawdhry/copier-fastapi-webservice backup-service
```

Use a new destination for each example. The project name determines the default slug, package and CLI command.

## Run locally

```bash
cd backup-service
git init -b main
task setup
cp .env.example .env
uv run backup-service init-db
task doctor
task dev
```

If jobs are enabled, start Redis before starting the API. See [Background Jobs](Background-Jobs).

In another terminal:

```bash
curl -fsS http://127.0.0.1:8000/health/ready
uv run backup-service resources
```

Keep the generated uv.lock in Git. For released templates, select a reviewed tag instead of HEAD when available.
