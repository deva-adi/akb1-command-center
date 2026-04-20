"""Tab 7 AI Governance read endpoints (8 tables)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import (
    AiCodeMetrics,
    AiGovernanceConfig,
    AiOverrideLog,
    AiSdlcMetrics,
    AiTool,
    AiToolAssignment,
    AiTrustScore,
    AiUsageMetrics,
)
from app.schemas.ai import (
    AiCodeMetricsOut,
    AiGovernanceConfigOut,
    AiOverrideOut,
    AiSdlcMetricsOut,
    AiToolAssignmentOut,
    AiToolOut,
    AiTrustScoreOut,
    AiUsageOut,
)

tools_router = APIRouter(prefix="/ai/tools", tags=["ai"])
assignments_router = APIRouter(prefix="/ai/assignments", tags=["ai"])
usage_router = APIRouter(prefix="/ai/usage", tags=["ai"])
code_metrics_router = APIRouter(prefix="/ai/code-metrics", tags=["ai"])
sdlc_metrics_router = APIRouter(prefix="/ai/sdlc-metrics", tags=["ai"])
trust_router = APIRouter(prefix="/ai/trust-scores", tags=["ai"])
governance_router = APIRouter(prefix="/ai/governance-config", tags=["ai"])
override_router = APIRouter(prefix="/ai/override-log", tags=["ai"])


@tools_router.get("", response_model=list[AiToolOut])
async def list_tools(session: AsyncSession = Depends(get_session)) -> list[AiTool]:
    result = await session.execute(select(AiTool).order_by(AiTool.name))
    return list(result.scalars().all())


@assignments_router.get("", response_model=list[AiToolAssignmentOut])
async def list_assignments(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AiToolAssignment]:
    stmt = select(AiToolAssignment)
    if program_id is not None:
        stmt = stmt.where(AiToolAssignment.program_id == program_id)
    return list((await session.execute(stmt)).scalars().all())


@usage_router.get("", response_model=list[AiUsageOut])
async def list_usage(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AiUsageMetrics]:
    stmt = select(AiUsageMetrics)
    if program_id is not None:
        stmt = stmt.where(AiUsageMetrics.program_id == program_id)
    stmt = stmt.order_by(AiUsageMetrics.snapshot_date.asc())
    return list((await session.execute(stmt)).scalars().all())


@code_metrics_router.get("", response_model=list[AiCodeMetricsOut])
async def list_code_metrics(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AiCodeMetrics]:
    stmt = select(AiCodeMetrics)
    if program_id is not None:
        stmt = stmt.where(AiCodeMetrics.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(AiCodeMetrics.project_id == project_id)
    stmt = stmt.order_by(AiCodeMetrics.sprint_number.asc().nulls_last())
    return list((await session.execute(stmt)).scalars().all())


@sdlc_metrics_router.get("", response_model=list[AiSdlcMetricsOut])
async def list_sdlc_metrics(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AiSdlcMetrics]:
    stmt = select(AiSdlcMetrics)
    if program_id is not None:
        stmt = stmt.where(AiSdlcMetrics.program_id == program_id)
    stmt = stmt.order_by(AiSdlcMetrics.sprint_number.asc().nulls_last())
    return list((await session.execute(stmt)).scalars().all())


@trust_router.get("", response_model=list[AiTrustScoreOut])
async def list_trust_scores(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AiTrustScore]:
    stmt = select(AiTrustScore)
    if program_id is not None:
        stmt = stmt.where(AiTrustScore.program_id == program_id)
    return list((await session.execute(stmt)).scalars().all())


@governance_router.get("", response_model=list[AiGovernanceConfigOut])
async def list_governance(
    program_id: int | None = Query(default=None),
    config_type: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AiGovernanceConfig]:
    stmt = select(AiGovernanceConfig)
    if program_id is not None:
        stmt = stmt.where(AiGovernanceConfig.program_id == program_id)
    if config_type is not None:
        stmt = stmt.where(AiGovernanceConfig.config_type == config_type)
    return list((await session.execute(stmt)).scalars().all())


@override_router.get("", response_model=list[AiOverrideOut])
async def list_overrides(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[AiOverrideLog]:
    stmt = select(AiOverrideLog)
    if program_id is not None:
        stmt = stmt.where(AiOverrideLog.program_id == program_id)
    stmt = stmt.order_by(AiOverrideLog.override_date.desc().nulls_last())
    return list((await session.execute(stmt)).scalars().all())
