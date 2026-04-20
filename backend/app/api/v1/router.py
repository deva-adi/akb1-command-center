from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import (
    currency,
    customer,
    data_import,
    health,
    kpi,
    programmes,
    risks,
    settings,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(programmes.router)
api_router.include_router(kpi.router)
api_router.include_router(risks.router)
api_router.include_router(customer.router)
api_router.include_router(currency.router)
api_router.include_router(settings.router)
api_router.include_router(data_import.router)
