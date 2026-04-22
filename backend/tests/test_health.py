from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_reports_table_count(app_client: AsyncClient) -> None:
    from app.models import TABLE_COUNT

    response = await app_client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    # Read TABLE_COUNT dynamically so this test does not go stale again when
    # we add tables in later releases.
    assert body["tables"] == TABLE_COUNT
    assert body["version"] == "5.2.0"


@pytest.mark.asyncio
async def test_health_endpoint_also_available_under_api_v1(app_client: AsyncClient) -> None:
    response = await app_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
