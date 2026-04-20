from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import data_import, health, kpi, programmes, settings

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(programmes.router)
api_router.include_router(kpi.router)
api_router.include_router(settings.router)
api_router.include_router(data_import.router)
