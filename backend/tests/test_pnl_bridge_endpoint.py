"""Integration tests for GET /api/v1/pnl/bridge/{metric_key}.

The PHOENIX Feb to Mar gross-margin delta test is the M2 reconciliation
gate measured through the endpoint, not just through the engine. This is
what guarantees the HTTP contract matches the seed.
"""
from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommercialScenario, Program, ProgrammeRate


async def _seed_phoenix_feb_mar(session: AsyncSession) -> int:
    p = Program(name="Phoenix", code="PHOENIX", start_date=date(2025, 4, 1))
    session.add(p)
    await session.flush()
    session.add_all(
        [
            CommercialScenario(
                program_id=p.id,
                scenario_name="Monthly Actuals",
                snapshot_date=date(2026, 2, 1),
                planned_revenue=850_000,
                actual_revenue=845_000,
                planned_cost=540_000,
                actual_cost=555_000,
                gross_margin_pct=0.314,
                contribution_margin_pct=0.182,
                portfolio_margin_pct=0.108,
                net_margin_pct=0.062,
            ),
            CommercialScenario(
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
            ),
        ]
    )
    # Plausible tier snapshots at Feb and Mar so Price and Mix drivers
    # have real numbers to work with.
    for tier, planned, actual_feb, actual_mar, weight_feb, weight_mar in [
        ("Junior", 70.0, 70.0, 72.0, 0.40, 0.50),
        ("Mid", 110.0, 114.0, 118.0, 0.45, 0.33),
        ("Senior", 180.0, 178.0, 175.0, 0.15, 0.17),
    ]:
        session.add(
            ProgrammeRate(
                program_code="PHOENIX",
                snapshot_date=date(2026, 2, 1),
                role_tier=tier,
                planned_rate=planned,
                actual_rate=actual_feb,
                tier_weight_planned=0.30 if tier == "Junior" else (0.50 if tier == "Mid" else 0.20),
                tier_weight_actual=weight_feb,
            )
        )
        session.add(
            ProgrammeRate(
                program_code="PHOENIX",
                snapshot_date=date(2026, 3, 1),
                role_tier=tier,
                planned_rate=planned,
                actual_rate=actual_mar,
                tier_weight_planned=0.30 if tier == "Junior" else (0.50 if tier == "Mid" else 0.20),
                tier_weight_actual=weight_mar,
            )
        )
    await session.commit()
    return p.id


@pytest.mark.asyncio
async def test_bridge_phoenix_feb_to_mar_total_delta_is_minus_340_bps(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        params={
            "programme": "PHOENIX",
            "from": "2026-02-01",
            "to": "2026-03-01",
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["programme_code"] == "PHOENIX"
    assert body["metric_key"] == "pnl.gross_margin_pct.programme.month"
    assert body["prior_value"] == 0.314
    assert body["current_value"] == 0.28
    assert abs(body["total_delta_bps"] - (-340.0)) < 1.0


@pytest.mark.asyncio
async def test_bridge_drivers_sum_to_total_delta_exactly(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        params={"programme": "PHOENIX", "from": "2026-02-01", "to": "2026-03-01"},
    )
    body = r.json()
    drivers = body["drivers"]
    driver_sum = (
        drivers["price_bps"]
        + drivers["volume_bps"]
        + drivers["mix_bps"]
        + drivers["cost_bps_residual"]
    )
    assert abs(driver_sum - body["total_delta_bps"]) < 0.01


@pytest.mark.asyncio
async def test_bridge_rejects_unsupported_metric_with_422(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/pnl.cpi.programme.month",
        params={"programme": "PHOENIX", "from": "2026-02-01", "to": "2026-03-01"},
    )
    assert r.status_code == 422
    body = r.json()
    # Generic unprocessable_entity because the HTTPException carries the
    # detail. Either way the envelope is populated.
    assert body["error"]["code"] in {"unprocessable_entity", "bad_filter_value", "bad_lineage_key"}


@pytest.mark.asyncio
async def test_bridge_rejects_malformed_lineage_key_with_422(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/not-a-valid-key",
        params={"programme": "PHOENIX", "from": "2026-02-01", "to": "2026-03-01"},
    )
    assert r.status_code == 422
    body = r.json()
    assert body["error"]["code"] == "bad_lineage_key"


@pytest.mark.asyncio
async def test_bridge_requires_programme_filter(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        params={"from": "2026-02-01", "to": "2026-03-01"},
    )
    assert r.status_code == 400
    body = r.json()
    assert body["error"]["code"] == "bad_request"


@pytest.mark.asyncio
async def test_bridge_requires_from_and_to(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        params={"programme": "PHOENIX", "from": "2026-02-01"},
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_bridge_missing_snapshot_row_returns_404(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        params={
            "programme": "PHOENIX",
            "from": "2030-01-01",
            "to": "2030-02-01",
        },
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_bridge_malformed_date_filter_returns_422_envelope(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix_feb_mar(session)
    r = await app_client.get(
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        params={
            "programme": "PHOENIX",
            "from": "not-a-date",
            "to": "2026-03-01",
        },
    )
    assert r.status_code == 422
    body = r.json()
    assert body["error"]["code"] == "bad_filter_value"
    assert body["error"]["details"]["field"] == "from"
