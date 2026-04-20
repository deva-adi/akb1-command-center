from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_reports_table_count(app_client: AsyncClient) -> None:
    response = await app_client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["tables"] == 42
    assert body["version"] == "5.2.0"


@pytest.mark.asyncio
async def test_health_endpoint_also_available_under_api_v1(app_client: AsyncClient) -> None:
    response = await app_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
