"""Lifecycle probes shared by all three processes."""

import sys
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Literal

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from packages.platform.config import Settings

ServiceName = Literal["api", "worker", "mcp"]


@dataclass
class ServiceState:
    ready: bool = False


def create_service_app(service: ServiceName, settings: Settings | None = None) -> FastAPI:
    # Validate even if the caller only uses the ASGI factory.
    if settings is None:
        Settings()
    state = ServiceState()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        state.ready = True
        try:
            yield
        finally:
            state.ready = False

    app = FastAPI(title=f"Procurement {service}", lifespan=lifespan)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": service}

    @app.get("/ready")
    def ready() -> JSONResponse:
        return JSONResponse(
            {"status": "ready" if state.ready else "not_ready", "service": service},
            status_code=200 if state.ready else 503,
        )

    return app


def run_service(service: ServiceName, factory: Callable[[Settings], FastAPI]) -> None:
    try:
        settings = Settings()
    except ValidationError as exc:
        # Never render field inputs; even future secret fields must remain private.
        fields = ", ".join(".".join(map(str, error["loc"])) for error in exc.errors())
        print(f"Invalid configuration ({fields}). Check PAW_ variables and .env.", file=sys.stderr)
        raise SystemExit(2) from None
    port = {"api": settings.api_port, "worker": settings.worker_port, "mcp": settings.mcp_port}[
        service
    ]
    uvicorn.run(factory(settings), host=settings.host, port=port, log_level=settings.log_level)
