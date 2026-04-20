from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Risk
from app.schemas.risk import RiskOut

router = APIRouter(prefix="/risks", tags=["risks"])


@router.get("", response_model=list[RiskOut])
async def list_risks(
    program_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    sort_by: str = Query(default="impact", pattern="^(impact|probability|created_at)$"),
    limit: int | None = Query(default=None, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
) -> list[Risk]:
    stmt = select(Risk)
    if program_id is not None:
        stmt = stmt.where(Risk.program_id == program_id)
    if status is not None:
        stmt = stmt.where(Risk.status == status)
    if sort_by == "impact":
        stmt = stmt.order_by(Risk.impact.desc().nulls_last())
    elif sort_by == "probability":
        stmt = stmt.order_by(Risk.probability.desc().nulls_last())
    else:
        stmt = stmt.order_by(Risk.created_at.desc())
    if limit is not None:
        stmt = stmt.limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())
