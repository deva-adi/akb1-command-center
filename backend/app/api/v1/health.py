from __future__ import annotations

from fastapi import APIRouter

from app.config import get_settings
from app.models import TABLE_COUNT
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        tables=TABLE_COUNT,
    )
