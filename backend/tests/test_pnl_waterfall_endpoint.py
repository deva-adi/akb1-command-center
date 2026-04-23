"""Integration tests for GET /api/v1/pnl/waterfall/{programme_code}."""
from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommercialScenario, Program


async def _seed_phoenix_mar_row(session: AsyncSession) -> int:
    """Insert a single Phoenix 2026-03-01 Monthly Actuals row matching the seed."""
    p = Program(name="Phoenix", code="PHOENIX", start_date=date(2025, 4, 1))
    session.add(p)
    await session.flush()
    cs = CommercialScenario(
        program_id=p.id,
        scenario_name="Monthly Actuals",
        snapshot_date=date(2026, 3, 1),
        planned_revenue=850_000,
        actual_revenue=820_000,
        planned_cost=550_000,
        actual_cost=590_000,
        gross_margin_pct=0.28,
        contribution_margin_pct=0.125,
        portfolio_margin_pct=0.082,
        net_margin_pct=0.041,
    )
    session.add(cs)
    await session.commit()
    return p.id


@pytest.mark.asyncio
async def test_waterfall_happy_path_returns_four_layers(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_mar_row(session)
    r = await app_client.get("/api/v1/pnl/waterfall/PHOENIX")
    assert r.status_code == 200
    body = r.json()
    assert body["programme_code"] == "PHOENIX"
    assert len(body["layers"]) == 4
    assert [layer["layer"] for layer in body["layers"]] == [
        "gross",
        "contribution",
        "portfolio",
        "net",
    ]
    assert body["revenue"] == 820_000
    assert body["layers"][0]["margin_pct"] == 0.28


@pytest.mark.asyncio
async def test_waterfall_emits_filters_applied_in_canonical_form(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_mar_row(session)
    r = await app_client.get(
        "/api/v1/pnl/waterfall/PHOENIX",
        params={"from": "2026-01-01", "to": "2026-03-31"},
    )
    assert r.status_code == 200
    applied = r.json()["filters_applied"]
    # Canonical-only keys present.
    assert "from" in applied
    assert "to" in applied
    # Aliases never surface.
    assert "period_start" not in applied
    assert "period_end" not in applied
    assert "programme_code" not in applied
    assert applied["from"] == "2026-01-01"
    assert applied["to"] == "2026-03-31"


@pytest.mark.asyncio
async def test_waterfall_accepts_alias_period_start_silently(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_mar_row(session)
    r = await app_client.get(
        "/api/v1/pnl/waterfall/PHOENIX",
        params={"period_start": "2026-01-01", "period_end": "2026-03-31"},
    )
    assert r.status_code == 200
    applied = r.json()["filters_applied"]
    assert applied["from"] == "2026-01-01"
    assert applied["to"] == "2026-03-31"


@pytest.mark.asyncio
async def test_waterfall_returns_lineage_block_with_one_entry(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_mar_row(session)
    r = await app_client.get("/api/v1/pnl/waterfall/PHOENIX")
    lineage = r.json()["lineage"]
    assert lineage["entries_total_count"] == 1
    assert lineage["sampling"] == "full"
    entry = lineage["entries"][0]
    assert entry["table"] == "commercial_scenarios"
    assert entry["program_code"] == "PHOENIX"
    assert entry["snapshot_date"] == "2026-03-01"


@pytest.mark.asyncio
async def test_waterfall_unknown_programme_returns_404_in_standard_envelope(
    app_client: AsyncClient,
) -> None:
    r = await app_client.get("/api/v1/pnl/waterfall/DOES_NOT_EXIST")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body
    assert body["error"]["code"] == "not_found"


@pytest.mark.asyncio
async def test_waterfall_malformed_filter_returns_422_with_envelope(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_mar_row(session)
    r = await app_client.get(
        "/api/v1/pnl/waterfall/PHOENIX",
        params={"from": "not-a-date"},
    )
    assert r.status_code == 422
    body = r.json()
    assert body["error"]["code"] == "bad_filter_value"
    assert body["error"]["details"]["field"] == "from"


@pytest.mark.asyncio
async def test_waterfall_no_matching_rows_returns_200_with_empty_layers(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_mar_row(session)
    r = await app_client.get(
        "/api/v1/pnl/waterfall/PHOENIX",
        params={"from": "2030-01-01", "to": "2030-12-31"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["layers"] == []
    assert body["revenue"] == 0.0
    assert body["filters_applied"]["from"] == "2030-01-01"
