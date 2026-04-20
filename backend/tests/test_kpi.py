from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import KpiDefinition


async def _seed_kpis(session: AsyncSession) -> dict[str, int]:
    delivery = KpiDefinition(
        name="Cost Performance Index",
        code="CPI",
        formula="EV / AC",
        unit="ratio",
        weight=1.2,
        category="Delivery",
        is_higher_better=True,
    )
    quality = KpiDefinition(
        name="Defect Density",
        code="DD",
        formula="defects / kloc",
        unit="count",
        weight=1.0,
        category="Quality",
        is_higher_better=False,
    )
    session.add_all([delivery, quality])
    await session.commit()
    return {"CPI": delivery.id, "DD": quality.id}


@pytest.mark.asyncio
async def test_kpi_category_filter(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    await _seed_kpis(session)
    response = await app_client.get(
        "/api/v1/kpi/definitions", params={"category": "Delivery"}
    )
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 1
    assert rows[0]["code"] == "CPI"


@pytest.mark.asyncio
async def test_kpi_weight_update(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    ids = await _seed_kpis(session)
    response = await app_client.put(
        f"/api/v1/kpi/definitions/{ids['CPI']}/weight", json={"weight": 2.5}
    )
    assert response.status_code == 200
    assert response.json()["weight"] == 2.5

    refreshed = await app_client.get(f"/api/v1/kpi/definitions/{ids['CPI']}")
    assert refreshed.status_code == 200
    assert refreshed.json()["weight"] == 2.5


@pytest.mark.asyncio
async def test_kpi_weight_update_rejects_out_of_range(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    ids = await _seed_kpis(session)
    response = await app_client.put(
        f"/api/v1/kpi/definitions/{ids['CPI']}/weight", json={"weight": 42.0}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_kpi_weight_update_404_on_missing_kpi(
    app_client: AsyncClient,
) -> None:
    response = await app_client.put(
        "/api/v1/kpi/definitions/9999/weight", json={"weight": 1.0}
    )
    assert response.status_code == 404
