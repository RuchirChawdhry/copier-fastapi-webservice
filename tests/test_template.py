"""Contract tests for generated services (no global environment modifications)."""

import tomllib
from pathlib import Path

import pytest
from copier import run_copy

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def generated(tmp_path: Path) -> Path:
    destination = tmp_path / "generated"
    run_copy(
        str(ROOT),
        destination,
        data={
            "project_name": "Demo Service",
            "project_slug": "demo-service",
            "package_name": "demo_service",
            "cli_command": "demo-service",
            "description": "A demo service.",
            "author_name": "Example Person",
        },
        defaults=True,
        unsafe=False,
    )
    return destination


def test_template_repo_has_no_active_actions() -> None:
    assert not (ROOT / ".github" / "workflows").exists()
    assert (ROOT / "template" / ".github" / "workflows" / "ci.yml.jinja").exists()


def test_generated_project_is_backend_only(generated: Path) -> None:
    with (generated / "pyproject.toml").open("rb") as stream:
        config = tomllib.load(stream)
    dependencies = config["project"]["dependencies"]
    for name in ("fastapi", "arq", "orjson", "loguru", "schedule", "rich", "cyclopts", "uvicorn"):
        assert any(dependency.split(">=")[0] == name for dependency in dependencies)
    assert config["project"]["scripts"]["demo-service"] == "demo_service.cli:app"
    assert (generated / ".python-version").read_text().strip() == "3.14.7"
    assert (generated / "src" / "demo_service" / "api.py").is_file()
    assert (generated / "src" / "demo_service" / "worker.py").is_file()
    assert (generated / "src" / "demo_service" / "scheduler.py").is_file()
    assert not (generated / "frontend").exists()
    assert not (generated / "copier.yml").exists()


def test_generated_ci_is_pr_only(generated: Path) -> None:
    workflow = (generated / ".github/workflows/ci.yml").read_text()
    assert "pull_request:" in workflow
    assert "workflow_dispatch:" not in workflow
    assert "  push:" not in workflow
    assert "  schedule:" not in workflow
    assert "RuchirChawdhry/ci-workflows/.github/workflows/python-cli.yml@main" in workflow
    assert "RuchirChawdhry/ci-workflows/.github/workflows/python-build.yml@main" in workflow


def test_generated_boot_installer_and_agent_guide(generated: Path) -> None:
    installer = (generated / "deploy/install.sh").read_text()
    assert "systemctl enable --now" in installer
    assert "Restart=always" in installer
    assert "WantedBy=multi-user.target" in installer
    assert (generated / "AGENTS.md").is_file()
    assert (generated / ".copier-answers.yml").is_file()
    assert (generated / ".env.example").is_file()
