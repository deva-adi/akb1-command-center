from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "AKB1 Command Center"
    app_version: str = "5.2.0"
    environment: str = Field(default="development")

    database_url: str = Field(default="sqlite+aiosqlite:///data/akb1.db")
    database_sync_url: str = Field(default="sqlite:///data/akb1.db")

    seed_demo_data: bool = Field(default=True)

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:9000"])

    log_level: str = Field(default="info")

    api_key_enabled: bool = Field(default=False)
    api_key_hash: str = Field(default="")

    rate_limit_read: str = Field(default="60/minute")
    rate_limit_write: str = Field(default="10/minute")
    rate_limit_upload: str = Field(default="5/minute")

    base_currency: str = Field(default="INR")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, v: object) -> object:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
