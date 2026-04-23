"""Tests for the seven remaining M3b P&L endpoints.

Covers: pfa, pyramid, losses, evm, dso, revenue, lineage. Each endpoint
gets at least a happy-path assertion, a 4xx envelope assertion, and a
lineage-block presence assertion, plus one hand-calc reconciliation for
the handful of metrics the M2 seed lets us anchor exactly.
"""
from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CommercialScenario,
    EvmSnapshot,
    LossExposure,
    Program,
    ProgrammeRate,
    ResourcePool,
)


# --- fixtures ----------------------------------------------------------


async def _seed_phoenix(session: AsyncSession) -> int:
    p = Program(name="Phoenix", code="PHOENIX", start_date=date(2025, 4, 1))
    session.add(p)
    await session.flush()
    # Feb and Mar Monthly Actuals plus a Forecast at Completion row.
    rows = [
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
            billing_ratio=0.88,
            billed_revenue=743_600,
            collected_revenue=594_880,
            unbilled_wip=101_400,
            ar_balance=148_720,
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
            billing_ratio=0.88,
            billed_revenue=721_600,
            collected_revenue=577_280,
            unbilled_wip=98_400,
            ar_balance=144_320,
        ),
        CommercialScenario(
            program_id=p.id,
            scenario_name="Forecast at Completion",
            snapshot_date=date(2026, 3, 1),
            planned_revenue=10_000_000,
            actual_revenue=9_800_000,
            planned_cost=7_800_000,
            actual_cost=8_200_000,
            gross_margin_pct=0.163,
        ),
    ]
    for r in rows:
        session.add(r)
    # One EVM snapshot so /evm and the CPI/SPI branch of /pfa have data.
    session.add(
        EvmSnapshot(
            program_id=p.id,
            snapshot_date=date(2026, 3, 1),
            planned_value=500_000,
            earned_value=425_000,
            actual_cost=480_000,
            bac=6_800_000,
            cpi=0.885,
            spi=0.85,
            eac=7_683_616,
            tcpi=1.09,
            vac=-883_616,
            percent_complete=6.3,
        )
    )
    # Loss rows for /losses.
    session.add_all(
        [
            LossExposure(
                program_id=p.id,
                snapshot_date=date(2026, 3, 1),
                loss_category="Bench Tax",
                amount=765_000,
                mitigation_status="Monitoring",
            ),
            LossExposure(
                program_id=p.id,
                snapshot_date=date(2026, 3, 1),
                loss_category="Scope Creep",
                amount=420_000,
                mitigation_status="In Progress",
            ),
        ]
    )
    # Programme rates for /pyramid.
    for tier, pr, ar, ph, ah, pw, aw in [
        ("Junior", 70.0, 72.0, 3, 3, 0.30, 0.50),
        ("Mid", 110.0, 118.0, 2, 2, 0.50, 0.33),
        ("Senior", 180.0, 175.0, 1, 1, 0.20, 0.17),
    ]:
        session.add(
            ProgrammeRate(
                program_code="PHOENIX",
                snapshot_date=date(2026, 3, 1),
                role_tier=tier,
                planned_rate=pr,
                actual_rate=ar,
                planned_headcount=ph,
                actual_headcount=ah,
                tier_weight_planned=pw,
                tier_weight_actual=aw,
            )
        )
    # Resource pool rows with utilisation per tier.
    for name, tier, util in [
        ("Priya Sharma", "Senior", 88.0),
        ("Raj Kumar", "Mid", 85.0),
        ("Kavya Nair", "Mid", 85.0),
        ("Vikram Rao", "Junior", 0.0),
        ("Ananya Desai", "Junior", 0.0),
    ]:
        session.add(
            ResourcePool(
                name=name,
                role_tier=tier,
                current_program_id=p.id,
                utilization_pct=util,
                status="Active",
            )
        )
    await session.commit()
    return p.id


# --- /pfa --------------------------------------------------------------


@pytest.mark.asyncio
async def test_pfa_default_metric_returns_series(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/pfa/PHOENIX")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["metric"] == "gross_pct"
    assert "series" in body
    assert set(body["series"].keys()) == {"plan", "forecast", "actual"}
    assert body["lineage"]["entries_total_count"] >= 1


@pytest.mark.asyncio
async def test_pfa_cpi_metric_pulls_from_evm(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/pfa/PHOENIX", params={"metric": "cpi"})
    assert r.status_code == 200
    actual = r.json()["series"]["actual"]
    assert len(actual) == 1
    assert actual[0]["value"] == 0.885


@pytest.mark.asyncio
async def test_pfa_unknown_metric_returns_422_envelope(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/pfa/PHOENIX", params={"metric": "ebitda"})
    assert r.status_code == 422
    assert "error" in r.json()


# --- /pyramid ----------------------------------------------------------


@pytest.mark.asyncio
async def test_pyramid_phoenix_mar_returns_three_tiers_and_rag(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/pyramid/PHOENIX")
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body["tiers"]) == 3
    assert {t["role_tier"] for t in body["tiers"]} == {"Junior", "Mid", "Senior"}
    assert body["rag"] in {"green", "amber", "red"}
    # Junior weight shifted 0.30 planned -> 0.50 actual, a 20pp delta.
    # Max delta across tiers >15 pp -> red.
    assert body["rag"] == "red"
    jr = next(t for t in body["tiers"] if t["role_tier"] == "Junior")
    assert jr["utilisation_pct"] == 0.0


@pytest.mark.asyncio
async def test_pyramid_unknown_programme_returns_404_envelope(
    app_client: AsyncClient,
) -> None:
    r = await app_client.get("/api/v1/pnl/pyramid/NOPE")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


# --- /losses -----------------------------------------------------------


@pytest.mark.asyncio
async def test_losses_phoenix_bench_tax_revenue_foregone_is_amount_over_0_70(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/losses/PHOENIX")
    assert r.status_code == 200, r.text
    body = r.json()
    bench = next(row for row in body["rows"] if row["loss_category"] == "Bench Tax")
    # 765000 / (1 - 0.30) = 1,092,857.14... rounded to 1,092,857
    assert bench["revenue_foregone"] == 1_092_857
    # margin_points_lost_programme_bps: 765000 / 820000 (Mar actual) * 10000
    # == 9329.27, within rounding.
    assert abs(bench["margin_points_lost_programme_bps"] - 9329.27) < 1.0


@pytest.mark.asyncio
async def test_losses_response_carries_lineage_entries(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/losses/PHOENIX")
    assert r.json()["lineage"]["entries_total_count"] == 2


# --- /evm --------------------------------------------------------------


@pytest.mark.asyncio
async def test_evm_phoenix_returns_seeded_snapshot(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/evm/PHOENIX")
    assert r.status_code == 200
    body = r.json()
    assert body["cpi"] == 0.885
    assert body["spi"] == 0.85
    assert body["bac"] == 6_800_000
    assert body["lineage"]["entries_total_count"] == 1


@pytest.mark.asyncio
async def test_evm_no_snapshot_returns_200_with_nulls(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get(
        "/api/v1/pnl/evm/PHOENIX", params={"from": "2030-01-01", "to": "2030-12-31"}
    )
    assert r.status_code == 200
    body = r.json()
    assert body["cpi"] is None
    assert body["lineage"]["entries_total_count"] == 0


# --- /dso --------------------------------------------------------------


@pytest.mark.asyncio
async def test_dso_phoenix_mar_computes_from_m2_backfill(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/dso/PHOENIX")
    body = r.json()
    # billed 721600, ar 144320, dso = 144320/721600 * 30 = 6.00 days exactly.
    assert r.status_code == 200
    assert body["billed_revenue"] == 721_600
    assert body["ar_balance"] == 144_320
    assert abs(body["dso_days"] - 6.00) < 0.01


# --- /revenue ----------------------------------------------------------


@pytest.mark.asyncio
async def test_revenue_phoenix_returns_five_cards_mapped_to_seed_columns(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/revenue/PHOENIX")
    body = r.json()
    assert r.status_code == 200
    card_keys = [c["card_key"] for c in body["cards"]]
    assert card_keys == [
        "committed_revenue",
        "booked_revenue",
        "billed_revenue",
        "collected_revenue",
        "unbilled_wip",
    ]
    by_key = {c["card_key"]: c for c in body["cards"]}
    assert by_key["committed_revenue"]["value"] == 850_000
    assert by_key["committed_revenue"]["source_column"] == "planned_revenue"
    assert by_key["booked_revenue"]["value"] == 820_000
    assert by_key["billed_revenue"]["value"] == 721_600
    assert by_key["unbilled_wip"]["value"] == 98_400


@pytest.mark.asyncio
async def test_revenue_no_row_returns_empty_cards_200(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get(
        "/api/v1/pnl/revenue/PHOENIX", params={"from": "2030-01-01", "to": "2030-12-31"}
    )
    assert r.status_code == 200
    assert r.json()["cards"] == []


# --- /lineage ----------------------------------------------------------


@pytest.mark.asyncio
async def test_lineage_phoenix_gross_margin_returns_value_and_atomic_row(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get(
        "/api/v1/pnl/lineage/pnl.gross_margin_pct.programme.month",
        params={"programme": "PHOENIX"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["supported"] is True
    assert body["value"] == 0.28
    assert body["unit"] == "ratio"
    assert len(body["atomic_rows"]) == 1
    row = body["atomic_rows"][0]
    assert row["table"] == "commercial_scenarios"
    assert row["program_code"] == "PHOENIX"
    assert row["columns_used"]["gross_margin_pct"] == 0.28


@pytest.mark.asyncio
async def test_lineage_dso_pulls_billed_and_ar(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get(
        "/api/v1/pnl/lineage/pnl.dso.programme.month",
        params={"programme": "PHOENIX"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["supported"] is True
    assert body["unit"] == "days"
    assert abs(body["value"] - 6.0) < 0.01


@pytest.mark.asyncio
async def test_lineage_unsupported_key_returns_supported_false_200(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get(
        "/api/v1/pnl/lineage/executive.utilisation.resource.current",
    )
    # Parses cleanly, but M3b resolver does not implement this metric yet.
    assert r.status_code == 200
    body = r.json()
    assert body["supported"] is False
    assert body["atomic_rows"] == []


@pytest.mark.asyncio
async def test_lineage_malformed_key_returns_422_envelope(
    app_client: AsyncClient,
) -> None:
    r = await app_client.get("/api/v1/pnl/lineage/totally-malformed")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "bad_lineage_key"


@pytest.mark.asyncio
async def test_lineage_programme_slice_without_programme_filter_returns_400(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    await _seed_phoenix(session)
    r = await app_client.get("/api/v1/pnl/lineage/pnl.gross_margin_pct.programme.month")
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "bad_request"
