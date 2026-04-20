from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import CurrencyRate
from app.schemas.currency import CurrencyRateOut

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/rates", response_model=list[CurrencyRateOut])
async def list_rates(session: AsyncSession = Depends(get_session)) -> list[CurrencyRate]:
    """Return configured FX rates relative to the USD base.

    Rates are seeded at install time (point-in-time, 2026-04-20). A live
    refresh endpoint against an external FX feed is planned but is deferred
    until the egress allow-list decision is made — see docs/ROADMAP.md.
    """
    result = await session.execute(select(CurrencyRate).order_by(CurrencyRate.code))
    return list(result.scalars().all())
