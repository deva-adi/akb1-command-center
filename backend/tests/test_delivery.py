from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    EvmSnapshot,
    FlowMetrics,
    Milestone,
    Program,
    Project,
    ProjectPhase,
    SprintData,
)


async def _seed_minimal_project(session: AsyncSession) -> tuple[int, int]:
    programme = Program(
        name="Test programme",
        code="T1",
        start_date=date(2025, 4, 1),
    )
    session.add(programme)
    await session.flush()
    project = Project(
        program_id=programme.id,
        name="Test project",
        code="T1-P1",
        delivery_methodology="Scrum",
    )
    session.add(project)
    await session.flush()
    return programme.id, project.id


@pytest.mark.asyncio
async def test_sprints_filter_by_project(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    _, project_id = await _seed_minimal_project(session)
    session.add_all(
        [
            SprintData(
                project_id=project_id,
                sprint_number=1,
                planned_points=50,
                completed_points=48,
                velocity=48,
            ),
            SprintData(
                project_id=project_id,
                sprint_number=2,
                planned_points=50,
                completed_points=52,
                velocity=52,
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get("/api/v1/sprints", params={"project_id": project_id})
    assert resp.status_code == 200
    rows = resp.json()
    assert len(rows) == 2
    assert [r["sprint_number"] for r in rows] == [1, 2]


@pytest.mark.asyncio
async def test_evm_filter_by_project_sorted_ascending(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    _, project_id = await _seed_minimal_project(session)
    session.add_all(
        [
            EvmSnapshot(
                project_id=project_id,
                snapshot_date=date(2026, 3, 1),
                planned_value=200,
                earned_value=190,
                actual_cost=210,
                cpi=0.905,
                spi=0.95,
            ),
            EvmSnapshot(
                project_id=project_id,
                snapshot_date=date(2026, 1, 1),
                planned_value=100,
                earned_value=98,
                actual_cost=95,
                cpi=1.03,
                spi=0.98,
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get("/api/v1/evm", params={"project_id": project_id})
    assert resp.status_code == 200
    dates = [row["snapshot_date"] for row in resp.json()]
    assert dates == sorted(dates)


@pytest.mark.asyncio
async def test_flow_filter_by_project(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    _, project_id = await _seed_minimal_project(session)
    session.add(
        FlowMetrics(
            project_id=project_id,
            period_start=date(2026, 2, 1),
            period_end=date(2026, 2, 7),
            throughput_items=7,
        )
    )
    await session.commit()
    resp = await app_client.get("/api/v1/flow", params={"project_id": project_id})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


@pytest.mark.asyncio
async def test_phases_sorted_by_sequence(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    _, project_id = await _seed_minimal_project(session)
    session.add_all(
        [
            ProjectPhase(
                project_id=project_id,
                phase_name="Test",
                phase_sequence=4,
                gate_status="pending",
            ),
            ProjectPhase(
                project_id=project_id,
                phase_name="Requirements",
                phase_sequence=1,
                gate_status="passed",
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get("/api/v1/phases", params={"project_id": project_id})
    assert resp.status_code == 200
    names = [row["phase_name"] for row in resp.json()]
    assert names == ["Requirements", "Test"]


@pytest.mark.asyncio
async def test_milestones_sorted_by_planned_date(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    program_id, project_id = await _seed_minimal_project(session)
    session.add_all(
        [
            Milestone(
                program_id=program_id,
                project_id=project_id,
                name="Late",
                planned_date=date(2026, 9, 30),
                status="Pending",
            ),
            Milestone(
                program_id=program_id,
                project_id=project_id,
                name="Early",
                planned_date=date(2026, 5, 1),
                status="In Progress",
            ),
        ]
    )
    await session.commit()
    resp = await app_client.get(
        "/api/v1/milestones", params={"project_id": project_id}
    )
    assert resp.status_code == 200
    names = [row["name"] for row in resp.json()]
    assert names == ["Early", "Late"]
