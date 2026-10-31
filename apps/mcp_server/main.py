"""Run MCP lifecycle probes without pretending to expose MCP tools."""

from fastapi import FastAPI

from packages.platform.config import Settings
from packages.platform.service import create_service_app, run_service


def create_app(settings: Settings | None = None) -> FastAPI:
    return create_service_app("mcp", settings)


def main() -> None:
    run_service("mcp", create_app)


if __name__ == "__main__":
    main()
