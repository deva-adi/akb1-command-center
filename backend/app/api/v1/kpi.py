from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import KpiDefinition, KpiSnapshot
from app.schemas.kpi import KpiDefinitionOut, KpiSnapshotOut

router = APIRouter(prefix="/kpi", tags=["kpi"])


@router.get("/definitions", response_model=list[KpiDefinitionOut])
async def list_kpi_definitions(
    session: AsyncSession = Depends(get_session),
) -> list[KpiDefinition]:
    result = await session.execute(select(KpiDefinition).order_by(KpiDefinition.id))
    return list(result.scalars().all())


@router.get("/snapshots", response_model=list[KpiSnapshotOut])
async def list_kpi_snapshots(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    kpi_code: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[KpiSnapshot]:
    stmt = select(KpiSnapshot)
    if program_id is not None:
        stmt = stmt.where(KpiSnapshot.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(KpiSnapshot.project_id == project_id)
    if kpi_code is not None:
        kpi_stmt = select(KpiDefinition.id).where(KpiDefinition.code == kpi_code)
        kpi_id = (await session.execute(kpi_stmt)).scalar_one_or_none()
        if kpi_id is None:
            return []
        stmt = stmt.where(KpiSnapshot.kpi_id == kpi_id)
    result = await session.execute(stmt.order_by(KpiSnapshot.snapshot_date))
    return list(result.scalars().all())
