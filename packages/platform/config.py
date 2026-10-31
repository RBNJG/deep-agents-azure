"""Explicit local configuration; no credentials or cloud defaults."""

from typing import Annotated, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Port = Annotated[int, Field(ge=1, le=65535)]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PAW_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    environment_id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,62}$")
    profile: Literal["local"] = "local"
    host: str = Field(default="127.0.0.1", min_length=1)
    api_port: Port = 8000
    mcp_port: Port = 8001
    worker_port: Port = 8002
    log_level: Literal["critical", "error", "warning", "info", "debug"] = "info"
