# Development and CI

Use the generated Taskfile for consistent local commands. The Python version lives in .python-version.

| Command | Purpose |
| --- | --- |
| task setup | Sync dependencies and install Git hooks |
| task dev | Start API |
| task fix | Ruff auto-fix and formatting |
| task lint | Check lint and formatting |
| task typecheck | ty check src |
| task test | pytest without benchmark timing |
| task check | Lint, types and tests |
| task benchmark | Run benchmark suite |
| task build | Build wheel and source distribution |
| task doctor | JSON diagnostics |
| task resources | Machine memory and CLI process RSS |

## Examples

```bash
task fix
task check
uv run pytest tests/test_api.py -q --benchmark-disable
task benchmark
cat .benchmarks/latest.json
task build
```

Pre-commit formats staged Python files and sorts imports. Run task setup from a Git root to install hooks. Do not disable lint rules to pass CI.

The template uses centralized [ci-workflows](https://github.com/RuchirChawdhry/ci-workflows). Template CI renders all eight feature combinations for contract validation, with six representative full validation profiles. Checks include Ruff, ty, pytest, wheel build and installed CLI smoke tests. Redis integration uses a real Redis server; ntfy tests use a local HTTP test server.

Generated project CI runs on pull requests and delegates quality and distribution checks to shared workflows. Strict test-first development is not required; add focused regression tests and verify actual integration behavior.

The resources command reports CLI RSS, not the live server's RSS.
