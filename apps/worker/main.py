"""Run worker lifecycle probes; no job execution in B00.2."""

from fastapi import FastAPI

from packages.platform.config import Settings
from packages.platform.service import create_service_app, run_service


def create_app(settings: Settings | None = None) -> FastAPI:
    return create_service_app("worker", settings)


def main() -> None:
    run_service("worker", create_app)


if __name__ == "__main__":
    main()
