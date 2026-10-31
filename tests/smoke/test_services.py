"""Local ASGI checks; no model, database or Azure calls."""

from collections.abc import Callable
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from apps.api.main import create_app as create_api
from apps.mcp_server.main import create_app as create_mcp
from apps.worker.main import create_app as create_worker
from packages.platform.config import Settings

pytestmark = pytest.mark.local


@pytest.mark.parametrize(
    ("factory", "service"), [(create_api, "api"), (create_worker, "worker"), (create_mcp, "mcp")]
)
def test_lifecycle(factory: Callable[[Settings], FastAPI], service: str) -> None:
    app = factory(Settings(environment_id="test-demo", _env_file=None))
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok", "service": service}
    assert client.get("/ready").status_code == 503
    with client:
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready", "service": service}
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 503


@pytest.mark.parametrize("factory", [create_api, create_worker, create_mcp])
def test_factory_requires_environment(
    factory: Callable[[], FastAPI], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PAW_ENVIRONMENT_ID", raising=False)
    with pytest.raises(ValidationError, match="environment_id"):
        factory()


@pytest.mark.parametrize("port", [0, -1, 65536])
def test_invalid_port(port: int) -> None:
    with pytest.raises(ValidationError, match="api_port"):
        Settings(environment_id="test-demo", api_port=port, _env_file=None)


def test_unsupported_profile_is_rejected_without_disclosing_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PAW_PROFILE", "untrusted-input")
    with pytest.raises(ValidationError) as error:
        Settings(environment_id="test-demo", _env_file=None)
    assert "profile" in str(error.value)
    assert "untrusted-input" not in str(error.value)


def test_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PAW_ENVIRONMENT_ID", raising=False)
    monkeypatch.delenv("PAW_API_PORT", raising=False)
    config = tmp_path / ".env"
    config.write_text("PAW_ENVIRONMENT_ID=from-file\nPAW_API_PORT=8100\n", encoding="utf-8")
    settings = Settings(_env_file=config)
    assert settings.environment_id == "from-file"
    assert settings.api_port == 8100
