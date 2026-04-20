from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CommercialScenario,
    LossExposure,
    Program,
    RateCard,
    ScopeCreepLog,
    SprintVelocityBlendRule,
)


async def _seed_programme(session: AsyncSession) -> int:
    programme = Program(name="T", code="T1", start_date=date(2025, 4, 1))
    session.add(programme)
    await session.flush()
    await session.commit()
    return programme.id


@pytest.mark.asyncio
async def test_commercial_filter_by_program(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    program_id = await _seed_programme(session)
    session.add_all(
        [
            CommercialScenario(
                program_id=program_id,
                scenario_name="Q1",
                planned_revenue=100.0,
                actual_revenue=98.0,
                planned_cost=70.0,
                actual_cost=72.0,
                gross_margin_pct=0.26,
                snapshot_date=date(2025, 4, 1),
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get(
        "/api/v1/commercial", params={"program_id": program_id}
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1


@pytest.mark.asyncio
async def test_losses_sorted_by_amount_desc(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    program_id = await _seed_programme(session)
    session.add_all(
        [
            LossExposure(
                program_id=program_id,
                snapshot_date=date(2026, 3, 31),
                loss_category="Small",
                amount=10.0,
            ),
            LossExposure(
                program_id=program_id,
                snapshot_date=date(2026, 3, 31),
                loss_category="Large",
                amount=1000.0,
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get("/api/v1/losses", params={"program_id": program_id})
    names = [row["loss_category"] for row in resp.json()]
    assert names == ["Large", "Small"]


@pytest.mark.asyncio
async def test_rate_cards_grouped_by_programme(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    program_id = await _seed_programme(session)
    session.add_all(
        [
            RateCard(
                program_id=program_id,
                role_tier="Senior",
                planned_rate=150,
                actual_rate=160,
                snapshot_date=date(2026, 3, 31),
            ),
            RateCard(
                program_id=program_id,
                role_tier="Junior",
                planned_rate=60,
                actual_rate=60,
                snapshot_date=date(2026, 3, 31),
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get(
        "/api/v1/rate-cards", params={"program_id": program_id}
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_change_requests_ordered_desc(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    program_id = await _seed_programme(session)
    session.add_all(
        [
            ScopeCreepLog(
                program_id=program_id,
                cr_date=date(2026, 2, 1),
                cr_description="Older",
                status="Approved",
            ),
            ScopeCreepLog(
                program_id=program_id,
                cr_date=date(2026, 3, 1),
                cr_description="Newer",
                status="Pending",
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get(
        "/api/v1/change-requests", params={"program_id": program_id}
    )
    names = [row["cr_description"] for row in resp.json()]
    assert names == ["Newer", "Older"]


@pytest.mark.asyncio
async def test_blend_rules_filter(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    program_id = await _seed_programme(session)
    session.add(
        SprintVelocityBlendRule(
            program_id=program_id,
            gate_name="Quality parity",
            current_value=0.97,
            threshold=0.95,
            passed=True,
        )
    )
    await session.commit()
    resp = await app_client.get(
        "/api/v1/blend-rules", params={"program_id": program_id}
    )
    assert resp.status_code == 200
    assert resp.json()[0]["passed"] is True
