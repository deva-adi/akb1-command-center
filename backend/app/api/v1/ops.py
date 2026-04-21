"""Tab 8 Smart Ops + Tab 9 Risk & Audit endpoints."""
from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session, get_session_factory
from app.models import AuditLog, ResourcePool, ScenarioExecution
from app.schemas.ops import AuditLogOut, ResourcePoolOut, ScenarioExecutionOut

scenarios_router = APIRouter(prefix="/smart-ops/scenarios", tags=["ops"])
resources_router = APIRouter(prefix="/smart-ops/resources", tags=["ops"])
alerts_router = APIRouter(prefix="/smart-ops/alerts", tags=["ops"])
audit_router = APIRouter(prefix="/audit", tags=["audit"])

_ALERT_STATUSES = {"Active", "Monitoring"}


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


@alerts_router.get("/stream")
async def stream_alerts() -> StreamingResponse:
    """SSE stream of active Smart Ops alerts — polls the DB every 10 s.

    Clients should reconnect on error (EventSource does this automatically).
    Set proxy_buffering off in nginx for this location.
    """
    factory = get_session_factory()

    async def _generate():
        while True:
            async with factory() as session:
                stmt = (
                    select(ScenarioExecution)
                    .where(ScenarioExecution.status.in_(list(_ALERT_STATUSES)))
                    .order_by(ScenarioExecution.execution_date.desc())
                    .limit(20)
                )
                rows = list((await session.execute(stmt)).scalars().all())

            payload = json.dumps(
                [
                    {
                        "id": r.id,
                        "name": r.scenario_name,
                        "status": r.status,
                        "impact": r.financial_impact,
                        "date": r.execution_date.isoformat() if r.execution_date else None,
                    }
                    for r in rows
                ]
            )
            yield f"data: {payload}\n\n"
            await asyncio.sleep(10)

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


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
