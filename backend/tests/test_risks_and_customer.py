from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CustomerAction, CustomerExpectation, Program, Risk


async def _seed_one_programme(session: AsyncSession) -> int:
    programme = Program(
        name="Test programme",
        code="TEST",
        start_date=date(2026, 1, 1),
        status="At Risk",
    )
    session.add(programme)
    await session.flush()
    session.add_all(
        [
            Risk(
                program_id=programme.id,
                title="Low impact",
                impact=100.0,
                probability=0.2,
                severity="Low",
                status="Open",
            ),
            Risk(
                program_id=programme.id,
                title="High impact",
                impact=500_000.0,
                probability=0.7,
                severity="High",
                status="Open",
            ),
        ]
    )
    session.add(
        CustomerExpectation(
            program_id=programme.id,
            snapshot_date=date(2026, 3, 31),
            dimension="timeline",
            expected_score=9.0,
            delivered_score=6.0,
            gap=-3.0,
        )
    )
    session.add(
        CustomerAction(
            program_id=programme.id,
            description="Escalate vendor slip",
            status="Open",
            priority="P1",
            escalated=True,
            due_date=date(2026, 4, 10),
        )
    )
    await session.commit()
    return programme.id


@pytest.mark.asyncio
async def test_risks_sorted_by_impact_desc(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    await _seed_one_programme(session)
    response = await app_client.get("/api/v1/risks", params={"sort_by": "impact", "limit": 5})
    assert response.status_code == 200
    rows = response.json()
    assert [r["title"] for r in rows] == ["High impact", "Low impact"]


@pytest.mark.asyncio
async def test_customer_endpoints_404_on_unknown_programme(
    app_client: AsyncClient,
) -> None:
    for path in ("/api/v1/customer/999/expectations", "/api/v1/customer/999/actions"):
        response = await app_client.get(path)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_customer_endpoints_return_seeded_rows(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    program_id = await _seed_one_programme(session)

    expectations = await app_client.get(f"/api/v1/customer/{program_id}/expectations")
    assert expectations.status_code == 200
    exp_rows = expectations.json()
    assert len(exp_rows) == 1
    assert exp_rows[0]["dimension"] == "timeline"
    assert exp_rows[0]["gap"] == -3.0

    actions = await app_client.get(f"/api/v1/customer/{program_id}/actions")
    assert actions.status_code == 200
    act_rows = actions.json()
    assert len(act_rows) == 1
    assert act_rows[0]["escalated"] is True
    assert act_rows[0]["priority"] == "P1"
