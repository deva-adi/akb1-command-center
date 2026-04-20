from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import (
    CustomerAction,
    CustomerExpectation,
    CustomerSatisfaction,
    Program,
    SlaIncident,
)
from app.schemas.customer import (
    CustomerActionOut,
    CustomerExpectationOut,
    CustomerSatisfactionOut,
    SlaIncidentOut,
)

router = APIRouter(prefix="/customer", tags=["customer"])


async def _require_programme(session: AsyncSession, program_id: int) -> Program:
    programme = await session.get(Program, program_id)
    if programme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Programme not found"
        )
    return programme


@router.get(
    "/{program_id}/expectations", response_model=list[CustomerExpectationOut]
)
async def list_expectations(
    program_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[CustomerExpectation]:
    await _require_programme(session, program_id)
    stmt = (
        select(CustomerExpectation)
        .where(CustomerExpectation.program_id == program_id)
        .order_by(
            CustomerExpectation.snapshot_date.desc(),
            CustomerExpectation.dimension,
        )
    )
    return list((await session.execute(stmt)).scalars().all())


@router.get("/{program_id}/actions", response_model=list[CustomerActionOut])
async def list_actions(
    program_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[CustomerAction]:
    await _require_programme(session, program_id)
    stmt = (
        select(CustomerAction)
        .where(CustomerAction.program_id == program_id)
        .order_by(
            CustomerAction.escalated.desc(),
            CustomerAction.due_date.asc().nulls_last(),
        )
    )
    return list((await session.execute(stmt)).scalars().all())


@router.get(
    "/satisfaction",
    response_model=list[CustomerSatisfactionOut],
    tags=["customer"],
)
async def list_satisfaction(
    program_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> list[CustomerSatisfaction]:
    stmt = select(CustomerSatisfaction)
    if program_id is not None:
        stmt = stmt.where(CustomerSatisfaction.program_id == program_id)
    stmt = stmt.order_by(CustomerSatisfaction.snapshot_date.asc())
    return list((await session.execute(stmt)).scalars().all())


@router.get(
    "/sla-incidents",
    response_model=list[SlaIncidentOut],
    tags=["customer"],
)
async def list_sla_incidents(
    program_id: int | None = Query(default=None),
    breached_only: bool = Query(default=False),
    session: AsyncSession = Depends(get_session),
) -> list[SlaIncident]:
    stmt = select(SlaIncident)
    if program_id is not None:
        stmt = stmt.where(SlaIncident.program_id == program_id)
    if breached_only:
        stmt = stmt.where(SlaIncident.sla_breached.is_(True))
    stmt = stmt.order_by(SlaIncident.reported_at.desc())
    return list((await session.execute(stmt)).scalars().all())
