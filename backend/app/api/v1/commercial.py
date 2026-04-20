"""Tab 4 (Velocity & Flow) + Tab 5 (Margin & EVM) read endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import (
    CommercialScenario,
    LossExposure,
    RateCard,
    ScopeCreepLog,
    SprintVelocityBlendRule,
    SprintVelocityDual,
)
from app.schemas.commercial import (
    BlendRuleOut,
    ChangeRequestOut,
    CommercialScenarioOut,
    LossExposureOut,
    RateCardOut,
    SprintVelocityDualOut,
)

dual_velocity_router = APIRouter(prefix="/dual-velocity", tags=["velocity"])
blend_rules_router = APIRouter(prefix="/blend-rules", tags=["velocity"])
commercial_router = APIRouter(prefix="/commercial", tags=["margin"])
losses_router = APIRouter(prefix="/losses", tags=["margin"])
rate_cards_router = APIRouter(prefix="/rate-cards", tags=["margin"])
change_requests_router = APIRouter(prefix="/change-requests", tags=["margin"])


@dual_velocity_router.get("", response_model=list[SprintVelocityDualOut])
async def list_dual_velocity(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[SprintVelocityDual]:
    stmt = select(SprintVelocityDual)
    if program_id is not None:
        stmt = stmt.where(SprintVelocityDual.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(SprintVelocityDual.project_id == project_id)
    stmt = stmt.order_by(SprintVelocityDual.sprint_number.asc().nulls_last())
    return list((await session.execute(stmt)).scalars().all())


@blend_rules_router.get("", response_model=list[BlendRuleOut])
async def list_blend_rules(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[SprintVelocityBlendRule]:
    stmt = select(SprintVelocityBlendRule)
    if program_id is not None:
        stmt = stmt.where(SprintVelocityBlendRule.program_id == program_id)
    return list((await session.execute(stmt)).scalars().all())


@commercial_router.get("", response_model=list[CommercialScenarioOut])
async def list_commercial(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[CommercialScenario]:
    stmt = select(CommercialScenario)
    if program_id is not None:
        stmt = stmt.where(CommercialScenario.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(CommercialScenario.project_id == project_id)
    stmt = stmt.order_by(CommercialScenario.snapshot_date.asc())
    return list((await session.execute(stmt)).scalars().all())


@losses_router.get("", response_model=list[LossExposureOut])
async def list_losses(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[LossExposure]:
    stmt = select(LossExposure)
    if program_id is not None:
        stmt = stmt.where(LossExposure.program_id == program_id)
    stmt = stmt.order_by(LossExposure.amount.desc().nulls_last())
    return list((await session.execute(stmt)).scalars().all())


@rate_cards_router.get("", response_model=list[RateCardOut])
async def list_rate_cards(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[RateCard]:
    stmt = select(RateCard)
    if program_id is not None:
        stmt = stmt.where(RateCard.program_id == program_id)
    stmt = stmt.order_by(RateCard.program_id.asc(), RateCard.role_tier.asc())
    return list((await session.execute(stmt)).scalars().all())


@change_requests_router.get("", response_model=list[ChangeRequestOut])
async def list_change_requests(
    program_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[ScopeCreepLog]:
    stmt = select(ScopeCreepLog)
    if program_id is not None:
        stmt = stmt.where(ScopeCreepLog.program_id == program_id)
    if project_id is not None:
        stmt = stmt.where(ScopeCreepLog.project_id == project_id)
    stmt = stmt.order_by(ScopeCreepLog.cr_date.desc().nulls_last())
    return list((await session.execute(stmt)).scalars().all())
