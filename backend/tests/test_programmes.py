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


@pytest.mark.asyncio
async def test_get_programme_and_404(app_client: AsyncClient) -> None:
    r = await app_client.post(
        "/api/v1/programmes",
        json={"name": "Alpha", "code": "ALPHA-1", "start_date": "2026-01-01"},
    )
    assert r.status_code == 201
    prog_id = r.json()["id"]

    detail = await app_client.get(f"/api/v1/programmes/{prog_id}")
    assert detail.status_code == 200
    assert detail.json()["code"] == "ALPHA-1"

    missing = await app_client.get("/api/v1/programmes/99999")
    assert missing.status_code == 404


@pytest.mark.asyncio
async def test_create_project_and_list(app_client: AsyncClient) -> None:
    r = await app_client.post(
        "/api/v1/programmes",
        json={"name": "Beta", "code": "BETA-1", "start_date": "2026-01-01"},
    )
    prog_id = r.json()["id"]

    proj = await app_client.post(
        f"/api/v1/programmes/{prog_id}/projects",
        json={"name": "Phase 1", "code": "BETA-P1", "start_date": "2026-02-01"},
    )
    assert proj.status_code == 201
    assert proj.json()["code"] == "BETA-P1"

    projects = await app_client.get(f"/api/v1/programmes/{prog_id}/projects")
    assert projects.status_code == 200
    assert len(projects.json()) == 1


@pytest.mark.asyncio
async def test_create_project_404_unknown_programme(app_client: AsyncClient) -> None:
    r = await app_client.post(
        "/api/v1/programmes/99999/projects",
        json={"name": "Orphan", "code": "ORF-1", "start_date": "2026-01-01"},
    )
    assert r.status_code == 404
