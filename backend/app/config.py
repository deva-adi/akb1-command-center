from __future__ import annotations

from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _read_package_version() -> str:
    """Return the version string from the package single source of truth.

    The value lives in ``backend/app/__init__.py`` as ``__version__``. No
    other file carries a hardcoded version string. Import is lazy so the
    config module can be imported cleanly in contexts where the package
    attribute is not yet available.
    """
    from app import __version__

    return __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "AKB1 Command Center"
    app_version: str = Field(default_factory=_read_package_version)
    environment: str = Field(default="development")

    database_url: str = Field(default="sqlite+aiosqlite:///data/akb1.db")
    database_sync_url: str = Field(default="sqlite:///data/akb1.db")

    seed_demo_data: bool = Field(default=True)

    # Stored as comma-separated string so env parsing never tries JSON.
    cors_origins_raw: str = Field(
        default="http://localhost:9000",
        alias="CORS_ORIGINS",
    )

    log_level: str = Field(default="info")

    api_key_enabled: bool = Field(default=False)
    api_key_hash: str = Field(default="")

    rate_limit_read: str = Field(default="60/minute")
    rate_limit_write: str = Field(default="10/minute")
    rate_limit_upload: str = Field(default="5/minute")

    base_currency: str = Field(default="USD")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
