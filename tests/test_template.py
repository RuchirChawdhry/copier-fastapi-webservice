"""Validate all Copier feature combinations and centralized CI delegation."""

import tomllib
from pathlib import Path

import pytest
from copier import run_copy

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(params=[(True, False), (False, False), (True, True), (False, True)])
def generated(tmp_path: Path, request):
    jobs, mcp = request.param
    destination = tmp_path / "generated"
    run_copy(
        str(ROOT),
        destination,
        data={"project_name": "Demo Service", "enable_jobs": jobs, "enable_mcp": mcp},
        defaults=True,
        unsafe=False,
        vcs_ref="HEAD",
    )
    return destination, jobs, mcp


def test_generated_features(generated):
    root, enabled, mcp = generated
    config = tomllib.loads((root / "pyproject.toml").read_text())
    dependencies = config["project"]["dependencies"]
    assert "fastapi" in dependencies
    assert "pydantic-settings" in dependencies
    for name in ("taskiq", "taskiq-redis", "taskiq-fastapi", "redis"):
        assert any(dep.split(">=")[0] == name for dep in dependencies) == enabled
    assert not any(dep.startswith("arq") for dep in dependencies)
    assert "orjson" not in dependencies
    assert "uvicorn[standard]" in dependencies
    assert "psutil" in dependencies
    assert "httpx2" in config["dependency-groups"]["dev"]
    assert any(dep.startswith("fastmcp>=") for dep in dependencies) == mcp
    assert not any(dep.startswith("mcp>=") for dep in dependencies)
    assert (root / "src/demo_service/mcp_server.py").exists() == mcp
    assert (root / "tests/test_mcp.py").exists() == mcp
    assert {"pre-commit", "pytest-benchmark", "ty"} <= set(config["dependency-groups"]["dev"])
    assert (root / "Taskfile.yml").is_file()
    assert (root / ".pre-commit-config.yaml").is_file()
    package = root / "src" / "demo_service"
    for module in ("worker", "scheduler", "jobs", "queue"):
        assert (package / f"{module}.py").exists() == enabled
    for name in ("worker", "scheduler"):
        assert (root / "tests" / f"test_{name}.py").exists() == enabled
    assert (root / ".python-version").read_text() == (ROOT / "template/.python-version").read_text()
    assert ("REDIS_URL" in (root / ".env.example").read_text()) == enabled
    assert ('write_unit worker' in (root / "deploy/install.sh").read_text()) == enabled
    assert not (root / "frontend").exists()
    assert not list(root.rglob("*.jinja"))
    for path in root.rglob("*.py"):
        compile(path.read_text(), str(path), "exec")


def test_ci_contract(generated):
    root, _, _ = generated
    workflow = (root / ".github/workflows/ci.yml").read_text()
    assert "pull_request:" in workflow
    assert "workflow_dispatch:" not in workflow
    assert "  push:" not in workflow
    assert ".python-version" in workflow
    assert "ci-workflows/.github/workflows/python-cli.yml@main" in workflow
    assert "ci-workflows/.github/workflows/python-build.yml@main" in workflow
    assert "ci-workflows/.github/workflows/copier-ci.yml@main" in (
        ROOT / ".github/workflows/template-ci.yml"
    ).read_text()
