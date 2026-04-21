from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import KpiDefinition, KpiSnapshot, Program


@pytest.mark.asyncio
async def test_schemas_endpoint_lists_supported_entities(
    app_client: AsyncClient,
) -> None:
    resp = await app_client.get("/api/v1/import/schemas")
    assert resp.status_code == 200
    body = resp.json()
    assert "programmes" in body
    assert "kpi_monthly" in body
    assert "expected_columns" in body["programmes"]


@pytest.mark.asyncio
async def test_programmes_commit_and_rollback(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    # Seed one existing programme so we can prove rollback also reverts
    # an update, not just a brand-new insert.
    existing = Program(
        name="Phoenix Platform Modernization",
        code="PHOENIX",
        client="GlobalBank Corp",
        start_date=date(2025, 4, 1),
        status="Active",
        bac=10_000_000,
        revenue=10_000_000,
        team_size=25,
        currency_code="INR",
    )
    session.add(existing)
    await session.commit()

    csv_body = (
        "name,code,client,start_date,status,bac,revenue,team_size,currency_code\n"
        "Phoenix Platform Modernization,PHOENIX,GlobalBank Corp,2025-04-01,At Risk,10500000,10500000,26,INR\n"
        "Atlas Cloud Migration,ATLAS,GlobalBank Corp,2025-06-01,Active,8000000,8000000,18,INR\n"
    )

    commit = await app_client.post(
        "/api/v1/import/csv/commit",
        data={"entity_type": "programmes"},
        files={"file": ("programmes.csv", csv_body, "text/csv")},
    )
    assert commit.status_code == 201, commit.text
    import_id = commit.json()["import_id"]
    assert commit.json()["rows_imported"] == 2
    assert commit.json()["affected_tables"] == ["programs"]

    # After commit: PHOENIX status flipped to At Risk, ATLAS created.
    session.expunge_all()
    phoenix = (
        await session.execute(select(Program).where(Program.code == "PHOENIX"))
    ).scalar_one()
    assert phoenix.status == "At Risk"
    atlas = (
        await session.execute(select(Program).where(Program.code == "ATLAS"))
    ).scalar_one()
    assert atlas is not None

    # Rollback — PHOENIX status should revert.
    rollback = await app_client.post(f"/api/v1/import/{import_id}/rollback")
    assert rollback.status_code == 200, rollback.text
    assert rollback.json()["status"] == "rolled_back"
    session.expunge_all()
    phoenix = (
        await session.execute(select(Program).where(Program.code == "PHOENIX"))
    ).scalar_one()
    assert phoenix.status == "Active"


@pytest.mark.asyncio
async def test_kpi_monthly_commit_and_rollback(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    programme = Program(
        name="Phoenix",
        code="PHOENIX",
        start_date=date(2025, 4, 1),
    )
    kpi = KpiDefinition(
        name="CPI",
        code="CPI",
        formula="EV / AC",
        unit="ratio",
        weight=1.0,
        is_higher_better=True,
    )
    session.add_all([programme, kpi])
    await session.flush()
    # Existing snapshot — rollback should keep this value.
    session.add(
        KpiSnapshot(
            program_id=programme.id,
            kpi_id=kpi.id,
            snapshot_date=date(2026, 1, 1),
            value=0.95,
            trend="flat",
        )
    )
    await session.commit()

    csv_body = (
        "program_code,kpi_code,snapshot_date,value,notes\n"
        "PHOENIX,CPI,2026-01-01,0.80,CSV override\n"
        "PHOENIX,CPI,2026-02-01,0.82,New month\n"
    )

    commit = await app_client.post(
        "/api/v1/import/csv/commit",
        data={"entity_type": "kpi_monthly"},
        files={"file": ("kpi_monthly.csv", csv_body, "text/csv")},
    )
    assert commit.status_code == 201, commit.text
    import_id = commit.json()["import_id"]

    # After commit: Jan value overwritten to 0.80, Feb row added.
    session.expunge_all()
    jan = (
        await session.execute(
            select(KpiSnapshot).where(
                KpiSnapshot.program_id == programme.id,
                KpiSnapshot.kpi_id == kpi.id,
                KpiSnapshot.snapshot_date == date(2026, 1, 1),
            )
        )
    ).scalar_one()
    assert jan.value == pytest.approx(0.80)

    # Rollback: Jan value restored to 0.95; Feb row wiped.
    rollback = await app_client.post(f"/api/v1/import/{import_id}/rollback")
    assert rollback.status_code == 200, rollback.text
    session.expunge_all()
    jan = (
        await session.execute(
            select(KpiSnapshot).where(
                KpiSnapshot.program_id == programme.id,
                KpiSnapshot.kpi_id == kpi.id,
                KpiSnapshot.snapshot_date == date(2026, 1, 1),
            )
        )
    ).scalar_one()
    assert jan.value == pytest.approx(0.95)
    feb = (
        await session.execute(
            select(KpiSnapshot).where(
                KpiSnapshot.program_id == programme.id,
                KpiSnapshot.kpi_id == kpi.id,
                KpiSnapshot.snapshot_date == date(2026, 2, 1),
            )
        )
    ).scalar_one_or_none()
    assert feb is None


@pytest.mark.asyncio
async def test_rollback_twice_rejected(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    session.add(
        Program(name="Atlas", code="ATLAS", start_date=date(2025, 6, 1))
    )
    await session.commit()
    csv_body = (
        "name,code,start_date\n"
        "Atlas Migration,ATLAS,2025-06-01\n"
    )
    commit = await app_client.post(
        "/api/v1/import/csv/commit",
        data={"entity_type": "programmes"},
        files={"file": ("programmes.csv", csv_body, "text/csv")},
    )
    import_id = commit.json()["import_id"]
    first = await app_client.post(f"/api/v1/import/{import_id}/rollback")
    assert first.status_code == 200
    second = await app_client.post(f"/api/v1/import/{import_id}/rollback")
    assert second.status_code == 400
