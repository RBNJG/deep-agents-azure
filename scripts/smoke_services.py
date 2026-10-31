"""Check real local HTTP processes; never invoke a model or provision services."""

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

SERVICES = {
    "api": ("apps.api.main", "PAW_API_PORT"),
    "worker": ("apps.worker.main", "PAW_WORKER_PORT"),
    "mcp": ("apps.mcp_server.main", "PAW_MCP_PORT"),
}


def available_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def main() -> None:
    # Isolate from the developer's .env and PAW_ variables.
    environment = {key: value for key, value in os.environ.items() if not key.startswith("PAW_")}
    environment.update(
        PAW_ENVIRONMENT_ID="local-smoke", PAW_HOST="127.0.0.1", PYTHONIOENCODING="utf-8"
    )
    with tempfile.TemporaryDirectory(prefix="paw-smoke-") as directory:
        for service, (module, port_variable) in SERVICES.items():
            port = available_port()
            service_env = {**environment, port_variable: str(port)}
            with Path(directory, f"{service}.log").open("w+", encoding="utf-8") as log:
                process = subprocess.Popen(
                    [sys.executable, "-m", module],
                    cwd=directory,
                    env=service_env,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                )
                try:
                    deadline = time.monotonic() + 20
                    while True:
                        if process.poll() is not None:
                            log.seek(0)
                            raise RuntimeError(f"{service} exited early: {log.read()}")
                        try:
                            for endpoint in ("health", "ready"):
                                with urllib.request.urlopen(
                                    f"http://127.0.0.1:{port}/{endpoint}", timeout=1
                                ) as response:
                                    result = json.load(response)
                                    if response.status != 200 or result["service"] != service:
                                        raise RuntimeError(f"Invalid {service}/{endpoint} response")
                            break
                        except (urllib.error.URLError, TimeoutError):
                            if time.monotonic() >= deadline:
                                log.seek(0)
                                raise RuntimeError(
                                    f"{service} did not become ready: {log.read()}"
                                ) from None
                            time.sleep(0.1)
                    print(f"{service}: /health=200 /ready=200 (real local HTTP)", flush=True)
                finally:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=5)


if __name__ == "__main__":
    main()
