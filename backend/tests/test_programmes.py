from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_programme(app_client: AsyncClient) -> None:
    payload = {
        "name": "Unit Test Programme",
        "code": "UTP-1",
        "client": "Test Co",
        "start_date": "2026-01-01",
    }
    created = await app_client.post("/api/v1/programmes", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["code"] == "UTP-1"

    listed = await app_client.get("/api/v1/programmes")
    assert listed.status_code == 200
    codes = [row["code"] for row in listed.json()]
    assert "UTP-1" in codes


@pytest.mark.asyncio
async def test_duplicate_programme_code_rejected(app_client: AsyncClient) -> None:
    payload = {"name": "Dup", "code": "DUP-1", "start_date": "2026-01-01"}
    first = await app_client.post("/api/v1/programmes", json=payload)
    assert first.status_code == 201
    second = await app_client.post("/api/v1/programmes", json=payload)
    assert second.status_code == 409
