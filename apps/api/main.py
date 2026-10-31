"""Run the API service shell."""

from fastapi import FastAPI

from packages.platform.config import Settings
from packages.platform.service import create_service_app, run_service


def create_app(settings: Settings | None = None) -> FastAPI:
    return create_service_app("api", settings)


def main() -> None:
    run_service("api", create_app)


if __name__ == "__main__":
    main()
