"""Installed entrypoint startup errors, isolated from a developer's config."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.local


@pytest.mark.parametrize("module", ["apps.api.main", "apps.worker.main", "apps.mcp_server.main"])
def test_entrypoint_fails_without_configuration(module: str, tmp_path: Path) -> None:
    environment = {key: value for key, value in os.environ.items() if not key.startswith("PAW_")}
    result = subprocess.run(
        [sys.executable, "-m", module],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 2
    assert "environment_id" in result.stderr
    assert "Invalid configuration" in result.stderr
    assert "Traceback" not in result.stderr
