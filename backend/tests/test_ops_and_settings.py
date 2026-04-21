from __future__ import annotations

from datetime import date, datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    AuditLog,
    KpiDefinition,
    KpiSnapshot,
    Program,
    ResourcePool,
    ScenarioExecution,
)


async def _seed_ops(session: AsyncSession) -> None:
    session.add_all([
        ScenarioExecution(
            scenario_name="Headcount cut 10%",
            status="Completed",
            execution_date=datetime(2026, 3, 1),
        ),
        ScenarioExecution(
            scenario_name="Rate card bump",
            status="Draft",
            execution_date=datetime(2026, 3, 15),
        ),
    ])
    session.add_all([
        ResourcePool(name="Alice", role="Architect", status="Bench", bench_days=14),
        ResourcePool(name="Bob", role="Developer", status="Deployed", bench_days=0),
    ])
    session.add_all([
        AuditLog(table_name="programmes", record_id=1, action="INSERT"),
        AuditLog(table_name="risks", record_id=5, action="UPDATE"),
    ])
    await session.commit()


@pytest.mark.asyncio
async def test_scenarios_list_all(session: AsyncSession, app_client: AsyncClient) -> None:
    await _seed_ops(session)
    r = await app_client.get("/api/v1/smart-ops/scenarios")
    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_scenarios_filter_by_status(session: AsyncSession, app_client: AsyncClient) -> None:
    await _seed_ops(session)
    r = await app_client.get("/api/v1/smart-ops/scenarios", params={"status": "Draft"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["scenario_name"] == "Rate card bump"


@pytest.mark.asyncio
async def test_resources_list_all(session: AsyncSession, app_client: AsyncClient) -> None:
    await _seed_ops(session)
    r = await app_client.get("/api/v1/smart-ops/resources")
    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_resources_bench_only(session: AsyncSession, app_client: AsyncClient) -> None:
    await _seed_ops(session)
    r = await app_client.get("/api/v1/smart-ops/resources", params={"bench_only": "true"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"


@pytest.mark.asyncio
async def test_audit_list_all(session: AsyncSession, app_client: AsyncClient) -> None:
    await _seed_ops(session)
    r = await app_client.get("/api/v1/audit")
    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_audit_filter_by_table(session: AsyncSession, app_client: AsyncClient) -> None:
    await _seed_ops(session)
    r = await app_client.get("/api/v1/audit", params={"table_name": "risks"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["table_name"] == "risks"


@pytest.mark.asyncio
async def test_settings_upsert_and_get(app_client: AsyncClient) -> None:
    r = await app_client.put("/api/v1/settings/theme", json={"value": "dark"})
    assert r.status_code == 200
    assert r.json()["value"] == "dark"

    r2 = await app_client.get("/api/v1/settings/theme")
    assert r2.status_code == 200
    assert r2.json()["key"] == "theme"


@pytest.mark.asyncio
async def test_settings_update_existing(app_client: AsyncClient) -> None:
    await app_client.put("/api/v1/settings/lang", json={"value": "en"})
    r = await app_client.put("/api/v1/settings/lang", json={"value": "fr"})
    assert r.status_code == 200
    assert r.json()["value"] == "fr"


@pytest.mark.asyncio
async def test_settings_get_404(app_client: AsyncClient) -> None:
    r = await app_client.get("/api/v1/settings/nonexistent_key_xyz")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_settings_list(app_client: AsyncClient) -> None:
    await app_client.put("/api/v1/settings/a", json={"value": "1"})
    await app_client.put("/api/v1/settings/b", json={"value": "2"})
    r = await app_client.get("/api/v1/settings")
    assert r.status_code == 200
    keys = [s["key"] for s in r.json()]
    assert "a" in keys
    assert "b" in keys


@pytest.mark.asyncio
async def test_kpi_snapshots_filter_by_kpi_code(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    prog = Program(name="P1", code="P1", start_date=date(2026, 1, 1), status="Green")
    session.add(prog)
    await session.flush()
    kpi = KpiDefinition(name="CPI", code="CPI2", formula="EV/AC", unit="ratio", weight=1.0, category="Delivery", is_higher_better=True)
    session.add(kpi)
    await session.flush()
    session.add(KpiSnapshot(program_id=prog.id, kpi_id=kpi.id, snapshot_date=date(2026, 3, 31), value=1.1))
    await session.commit()

    r = await app_client.get("/api/v1/kpi/snapshots", params={"kpi_code": "CPI2"})
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_kpi_snapshots_unknown_code_returns_empty(app_client: AsyncClient) -> None:
    r = await app_client.get("/api/v1/kpi/snapshots", params={"kpi_code": "UNKNOWN_XYZ"})
    assert r.status_code == 200
    assert r.json() == []
