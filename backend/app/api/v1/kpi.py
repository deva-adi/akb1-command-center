from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.models import KpiDefinition, KpiSnapshot
from app.rate_limit import limiter
from app.schemas.kpi import KpiDefinitionOut, KpiSnapshotOut, KpiWeightUpdate

router = APIRouter(prefix="/kpi", tags=["kpi"])
_write_limit = get_settings().rate_limit_write


@router.get("/definitions", response_model=list[KpiDefinitionOut])
async def list_kpi_definitions(
    category: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[KpiDefinition]:
    stmt = select(KpiDefinition).order_by(KpiDefinition.category, KpiDefinition.id)
    if category is not None:
        stmt = stmt.where(KpiDefinition.category == category)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@router.get("/definitions/{kpi_id}", response_model=KpiDefinitionOut)
async def get_kpi_definition(
    kpi_id: int,
    session: AsyncSession = Depends(get_session),
) -> KpiDefinition:
    kpi = await session.get(KpiDefinition, kpi_id)
    if kpi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI definition not found"
        )
    return kpi


@router.put("/definitions/{kpi_id}/weight", response_model=KpiDefinitionOut)
@limiter.limit(_write_limit)
async def update_kpi_weight(
    request: Request,
    kpi_id: int,
    payload: KpiWeightUpdate,
    session: AsyncSession = Depends(get_session),
) -> KpiDefinition:
    kpi = await session.get(KpiDefinition, kpi_id)
    if kpi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI definition not found"
        )
    kpi.weight = payload.weight
    await session.commit()
    await session.refresh(kpi)
    return kpi


@router.get("/snapshots", response_model=list[KpiSnapshotOut])
async def list_kpi_snapshots(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    kpi_code: str | None = Query(default=None),
    kpi_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[KpiSnapshot]:
    stmt = select(KpiSnapshot)
    if program_id is not None:
        stmt = stmt.where(KpiSnapshot.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(KpiSnapshot.project_id == project_id)
    if kpi_id is not None:
        stmt = stmt.where(KpiSnapshot.kpi_id == kpi_id)
    elif kpi_code is not None:
        kpi_stmt = select(KpiDefinition.id).where(KpiDefinition.code == kpi_code)
        resolved = (await session.execute(kpi_stmt)).scalar_one_or_none()
        if resolved is None:
            return []
        stmt = stmt.where(KpiSnapshot.kpi_id == resolved)
    result = await session.execute(stmt.order_by(KpiSnapshot.snapshot_date))
    return list(result.scalars().all())
