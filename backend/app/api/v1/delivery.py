"""Delivery-Health read endpoints — sprints, EVM, flow, phases, milestones.

All are GET-only and filter by program_id or project_id. Each router is
its own APIRouter so the /api/v1/router.py can mount them with distinct
prefixes (/sprints, /evm, /flow, /phases, /milestones).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import (
    EvmSnapshot,
    FlowMetrics,
    Milestone,
    ProjectPhase,
    SprintData,
)
from app.schemas.delivery import (
    EvmSnapshotOut,
    FlowMetricsOut,
    MilestoneOut,
    ProjectPhaseOut,
    SprintOut,
)

sprints_router = APIRouter(prefix="/sprints", tags=["delivery"])
evm_router = APIRouter(prefix="/evm", tags=["delivery"])
flow_router = APIRouter(prefix="/flow", tags=["delivery"])
phases_router = APIRouter(prefix="/phases", tags=["delivery"])
milestones_router = APIRouter(prefix="/milestones", tags=["delivery"])


@sprints_router.get("", response_model=list[SprintOut])
async def list_sprints(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[SprintData]:
    stmt = select(SprintData)
    if program_id is not None:
        stmt = stmt.where(SprintData.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(SprintData.project_id == project_id)
    stmt = stmt.order_by(SprintData.sprint_number.asc().nulls_last())
    return list((await session.execute(stmt)).scalars().all())


@evm_router.get("", response_model=list[EvmSnapshotOut])
async def list_evm(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[EvmSnapshot]:
    stmt = select(EvmSnapshot)
    if program_id is not None:
        stmt = stmt.where(EvmSnapshot.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(EvmSnapshot.project_id == project_id)
    stmt = stmt.order_by(EvmSnapshot.snapshot_date.asc())
    return list((await session.execute(stmt)).scalars().all())


@flow_router.get("", response_model=list[FlowMetricsOut])
async def list_flow(
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[FlowMetrics]:
    stmt = select(FlowMetrics)
    if project_id is not None:
        stmt = stmt.where(FlowMetrics.project_id == project_id)
    stmt = stmt.order_by(FlowMetrics.period_start.asc())
    return list((await session.execute(stmt)).scalars().all())


@phases_router.get("", response_model=list[ProjectPhaseOut])
async def list_phases(
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[ProjectPhase]:
    stmt = select(ProjectPhase)
    if project_id is not None:
        stmt = stmt.where(ProjectPhase.project_id == project_id)
    stmt = stmt.order_by(ProjectPhase.phase_sequence.asc())
    return list((await session.execute(stmt)).scalars().all())


@milestones_router.get("", response_model=list[MilestoneOut])
async def list_milestones(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[Milestone]:
    stmt = select(Milestone)
    if program_id is not None:
        stmt = stmt.where(Milestone.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(Milestone.project_id == project_id)
    stmt = stmt.order_by(Milestone.planned_date.asc())
    return list((await session.execute(stmt)).scalars().all())
