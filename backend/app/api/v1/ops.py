"""Tab 8 Smart Ops + Tab 9 Risk & Audit endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import AuditLog, ResourcePool, ScenarioExecution
from app.schemas.ops import AuditLogOut, ResourcePoolOut, ScenarioExecutionOut

scenarios_router = APIRouter(prefix="/smart-ops/scenarios", tags=["ops"])
resources_router = APIRouter(prefix="/smart-ops/resources", tags=["ops"])
audit_router = APIRouter(prefix="/audit", tags=["audit"])


@scenarios_router.get("", response_model=list[ScenarioExecutionOut])
async def list_scenarios(
    status: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[ScenarioExecution]:
    stmt = select(ScenarioExecution)
    if status is not None:
        stmt = stmt.where(ScenarioExecution.status == status)
    stmt = stmt.order_by(ScenarioExecution.execution_date.desc())
    return list((await session.execute(stmt)).scalars().all())


@resources_router.get("", response_model=list[ResourcePoolOut])
async def list_resources(
    bench_only: bool = Query(default=False),
    session: AsyncSession = Depends(get_session),
) -> list[ResourcePool]:
    stmt = select(ResourcePool)
    if bench_only:
        stmt = stmt.where(ResourcePool.status == "Bench")
    stmt = stmt.order_by(ResourcePool.bench_days.desc(), ResourcePool.name)
    return list((await session.execute(stmt)).scalars().all())


@audit_router.get("", response_model=list[AuditLogOut])
async def list_audit(
    table_name: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
) -> list[AuditLog]:
    stmt = select(AuditLog)
    if table_name is not None:
        stmt = stmt.where(AuditLog.table_name == table_name)
    stmt = stmt.order_by(AuditLog.timestamp.desc()).limit(limit)
    return list((await session.execute(stmt)).scalars().all())
