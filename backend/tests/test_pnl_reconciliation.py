"""M4 cross-endpoint reconciliation harness.

Purpose: prove that no two of the nine `/api/v1/pnl/` endpoints return
contradictory figures for the same programme and period. Each test
picks one cross-endpoint identity that must hold by construction, then
asserts it against the live HTTP responses.

Identities checked (per programme, per period unless noted):

    1. /revenue.booked_revenue   == /waterfall.revenue
    2. /revenue.billed_revenue   == /dso.billed_revenue
    3. /revenue.collected_revenue == /dso.collected_revenue
    4. /revenue.unbilled_wip     == /dso.unbilled_wip
    5. /revenue.committed_revenue == seed.planned_revenue
    6. /waterfall.layers[gross].margin_pct * /waterfall.revenue
        approx /waterfall.layers[gross].margin_value
    7. /lineage(pnl.gross_margin_pct.programme.month).value
        == /waterfall.layers[gross].margin_pct
    8. /lineage(pnl.dso.programme.month).value == /dso.dso_days
    9. /dso.ar_balance ==
        /dso.billed_revenue - /dso.collected_revenue
    10. /dso.dso_days == (ar_balance / billed_revenue) * 30
    11. /bridge: price + volume + mix + cost_residual == total_delta_bps
    12. /bridge.total_delta_bps ==
        (/bridge.current_value - /bridge.prior_value) * 10000
    13. /losses.programme_revenue == /waterfall.revenue
    14. /losses.rows[i].revenue_foregone ==
        round(amount / (1 - target_gross_margin_pct))
    15. /losses.rows[i].margin_points_lost_programme_bps ==
        amount / programme_revenue * 10000
    16. /evm: VAC == BAC - EAC within rounding
    17. /evm: CPI == EV / AC within rounding
    18. /pyramid: sum of tier_weight_actual == 1 within rounding
    19. /pfa.actual at current_snapshot == /waterfall.layers[gross].margin_pct
        (when metric == gross_pct)

Every test seeds Phoenix *and* Atlas so a programme-specific bug does
not hide. The harness is intentionally read-only (no mutation between
identity checks) so a regression in any one endpoint surfaces
immediately.
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests._pnl_fixtures import seed_novatech_m4


TARGET_GROSS_MARGIN_PCT = 0.30


# Query string shared by every endpoint that accepts programme scoping.
# Both seeded programmes have Monthly Actuals at 2026-03-01 and the
# Feb/Mar pair the bridge consumes.
_PERIOD_Q = {"from": "2026-03-01", "to": "2026-03-31"}
_BRIDGE_Q = {"from": "2026-02-01", "to": "2026-03-01"}


async def _get(client: AsyncClient, path: str, params: dict | None = None) -> dict:
    r = await client.get(path, params=params or {})
    assert r.status_code == 200, f"{path} -> {r.status_code}: {r.text}"
    return r.json()


# --- Revenue vs DSO vs Waterfall -------------------------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_revenue_booked_equals_waterfall_revenue(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    rev = await _get(app_client, f"/api/v1/pnl/revenue/{code}", _PERIOD_Q)
    wat = await _get(app_client, f"/api/v1/pnl/waterfall/{code}", _PERIOD_Q)
    booked = next(c for c in rev["cards"] if c["card_key"] == "booked_revenue")
    assert booked["value"] == wat["revenue"], (
        f"{code}: /revenue booked={booked['value']} but /waterfall revenue={wat['revenue']}"
    )


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_revenue_billed_equals_dso_billed(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    rev = await _get(app_client, f"/api/v1/pnl/revenue/{code}", _PERIOD_Q)
    dso = await _get(app_client, f"/api/v1/pnl/dso/{code}", _PERIOD_Q)
    billed = next(c for c in rev["cards"] if c["card_key"] == "billed_revenue")
    assert billed["value"] == dso["billed_revenue"]


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_revenue_collected_equals_dso_collected(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    rev = await _get(app_client, f"/api/v1/pnl/revenue/{code}", _PERIOD_Q)
    dso = await _get(app_client, f"/api/v1/pnl/dso/{code}", _PERIOD_Q)
    collected = next(c for c in rev["cards"] if c["card_key"] == "collected_revenue")
    assert collected["value"] == dso["collected_revenue"]


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_revenue_unbilled_equals_dso_unbilled(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    rev = await _get(app_client, f"/api/v1/pnl/revenue/{code}", _PERIOD_Q)
    dso = await _get(app_client, f"/api/v1/pnl/dso/{code}", _PERIOD_Q)
    unbilled = next(c for c in rev["cards"] if c["card_key"] == "unbilled_wip")
    assert unbilled["value"] == dso["unbilled_wip"]


@pytest.mark.asyncio
async def test_revenue_committed_equals_seed_planned(
    app_client: AsyncClient, session: AsyncSession
) -> None:
    seeds = await seed_novatech_m4(session)
    for code, seeded in seeds.items():
        rev = await _get(app_client, f"/api/v1/pnl/revenue/{code}", _PERIOD_Q)
        committed = next(c for c in rev["cards"] if c["card_key"] == "committed_revenue")
        assert committed["value"] == seeded.planned_revenue, (
            f"{code}: committed={committed['value']} vs seed.planned={seeded.planned_revenue}"
        )


# --- Waterfall internal identity + lineage parity --------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_waterfall_gross_margin_value_equals_pct_times_revenue(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    wat = await _get(app_client, f"/api/v1/pnl/waterfall/{code}", _PERIOD_Q)
    gross = next(l for l in wat["layers"] if l["layer"] == "gross")
    expected = round(gross["margin_pct"] * wat["revenue"], 2)
    assert abs(gross["margin_value"] - expected) < 1.0, (
        f"{code}: gross layer value {gross['margin_value']} vs pct*revenue {expected}"
    )


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_lineage_gross_margin_equals_waterfall_gross_pct(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    wat = await _get(app_client, f"/api/v1/pnl/waterfall/{code}", _PERIOD_Q)
    lin = await _get(
        app_client,
        "/api/v1/pnl/lineage/pnl.gross_margin_pct.programme.month",
        {"programme": code, **_PERIOD_Q},
    )
    gross = next(l for l in wat["layers"] if l["layer"] == "gross")
    assert lin["supported"] is True
    assert lin["value"] == gross["margin_pct"], (
        f"{code}: lineage value {lin['value']} vs waterfall gross_pct {gross['margin_pct']}"
    )


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_lineage_dso_equals_dso_endpoint(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    dso = await _get(app_client, f"/api/v1/pnl/dso/{code}", _PERIOD_Q)
    lin = await _get(
        app_client,
        "/api/v1/pnl/lineage/pnl.dso.programme.month",
        {"programme": code, **_PERIOD_Q},
    )
    assert lin["supported"] is True
    assert abs(lin["value"] - dso["dso_days"]) < 0.01


# --- DSO internal identity -------------------------------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_dso_ar_balance_equals_billed_minus_collected(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    dso = await _get(app_client, f"/api/v1/pnl/dso/{code}", _PERIOD_Q)
    assert dso["ar_balance"] == dso["billed_revenue"] - dso["collected_revenue"]


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_dso_days_matches_formula(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    dso = await _get(app_client, f"/api/v1/pnl/dso/{code}", _PERIOD_Q)
    expected = (dso["ar_balance"] / dso["billed_revenue"]) * 30
    assert abs(dso["dso_days"] - expected) < 0.01


# --- Bridge identities -----------------------------------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_bridge_four_drivers_sum_to_total_delta(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    br = await _get(
        app_client,
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        {"programme": code, **_BRIDGE_Q},
    )
    d = br["drivers"]
    identity = d["price_bps"] + d["volume_bps"] + d["mix_bps"] + d["cost_bps_residual"]
    assert abs(identity - br["total_delta_bps"]) < 0.01, (
        f"{code}: drivers sum {identity} vs total_delta_bps {br['total_delta_bps']}"
    )


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_bridge_total_delta_matches_current_minus_prior(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    br = await _get(
        app_client,
        "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
        {"programme": code, **_BRIDGE_Q},
    )
    expected = round((br["current_value"] - br["prior_value"]) * 10000, 2)
    assert abs(br["total_delta_bps"] - expected) < 0.01


# --- Losses attribution identities -----------------------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_losses_programme_revenue_equals_waterfall_revenue(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    wat = await _get(app_client, f"/api/v1/pnl/waterfall/{code}", _PERIOD_Q)
    losses = await _get(app_client, f"/api/v1/pnl/losses/{code}")
    assert losses["programme_revenue"] == wat["revenue"]


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_losses_revenue_foregone_matches_formula(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    losses = await _get(app_client, f"/api/v1/pnl/losses/{code}")
    target = losses["target_gross_margin_pct"]
    assert target == TARGET_GROSS_MARGIN_PCT
    for row in losses["rows"]:
        expected = round(row["amount"] / (1 - target))
        assert abs(row["revenue_foregone"] - expected) < 1.0, (
            f"{code}/{row['loss_category']}: foregone={row['revenue_foregone']} "
            f"expected={expected}"
        )


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_losses_programme_bps_matches_formula(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    losses = await _get(app_client, f"/api/v1/pnl/losses/{code}")
    prog_rev = losses["programme_revenue"]
    for row in losses["rows"]:
        expected = row["amount"] / prog_rev * 10000
        assert abs(row["margin_points_lost_programme_bps"] - expected) < 1.0


# --- EVM internal identities -----------------------------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_evm_vac_equals_bac_minus_eac(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    evm = await _get(app_client, f"/api/v1/pnl/evm/{code}", _PERIOD_Q)
    # Seed may round VAC to the nearest dollar; allow a 1-dollar tolerance.
    expected = evm["bac"] - evm["eac"]
    assert abs(evm["vac"] - expected) < 1.0, (
        f"{code}: VAC={evm['vac']} vs BAC-EAC={expected}"
    )


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_evm_cpi_equals_ev_over_ac(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    evm = await _get(app_client, f"/api/v1/pnl/evm/{code}", _PERIOD_Q)
    expected = evm["earned_value"] / evm["actual_cost"]
    # Seeded CPI rounds to three decimals; keep the tolerance at 0.005.
    assert abs(evm["cpi"] - expected) < 0.005


# --- Pyramid normalisation -------------------------------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_pyramid_actual_weights_sum_to_one(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    pyr = await _get(app_client, f"/api/v1/pnl/pyramid/{code}", _PERIOD_Q)
    total = sum((t.get("actual_weight") or 0.0) for t in pyr["tiers"])
    assert abs(total - 1.0) < 0.01, f"{code}: actual weights sum to {total}"


# --- PFA vs Waterfall (gross_pct metric) -----------------------------


@pytest.mark.parametrize("code", ["PHOENIX", "ATLAS"])
@pytest.mark.asyncio
async def test_pfa_gross_actual_matches_waterfall_gross(
    app_client: AsyncClient, session: AsyncSession, code: str
) -> None:
    await seed_novatech_m4(session)
    pfa = await _get(
        app_client, f"/api/v1/pnl/pfa/{code}", {"metric": "gross_pct"}
    )
    wat = await _get(app_client, f"/api/v1/pnl/waterfall/{code}", _PERIOD_Q)
    gross = next(l for l in wat["layers"] if l["layer"] == "gross")
    # The Mar actual point must match the waterfall gross for the same snapshot.
    mar_point = next(
        (p for p in pfa["series"]["actual"] if p["snapshot_date"] == "2026-03-01"),
        None,
    )
    assert mar_point is not None, f"{code}: no Mar actual in PFA series"
    assert abs(mar_point["value"] - gross["margin_pct"]) < 1e-6


# --- Every endpoint carries a non-empty lineage block ----------------


@pytest.mark.parametrize(
    "path,params",
    [
        ("/api/v1/pnl/waterfall/PHOENIX", _PERIOD_Q),
        (
            "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
            {"programme": "PHOENIX", **_BRIDGE_Q},
        ),
        ("/api/v1/pnl/pfa/PHOENIX", {"metric": "gross_pct"}),
        ("/api/v1/pnl/pyramid/PHOENIX", _PERIOD_Q),
        ("/api/v1/pnl/losses/PHOENIX", {}),
        ("/api/v1/pnl/evm/PHOENIX", _PERIOD_Q),
        ("/api/v1/pnl/dso/PHOENIX", _PERIOD_Q),
        ("/api/v1/pnl/revenue/PHOENIX", _PERIOD_Q),
        (
            "/api/v1/pnl/lineage/pnl.gross_margin_pct.programme.month",
            {"programme": "PHOENIX"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_every_endpoint_returns_a_lineage_block(
    app_client: AsyncClient,
    session: AsyncSession,
    path: str,
    params: dict,
) -> None:
    await seed_novatech_m4(session)
    body = await _get(app_client, path, params)
    assert "lineage" in body, f"{path} missing lineage block"
    lineage = body["lineage"]
    assert "formula" in lineage and isinstance(lineage["formula"], str)
    assert "entries_total_count" in lineage
    assert lineage["sampling"] in {"full", "sampled"}


# --- Every endpoint echoes filters_applied ---------------------------


@pytest.mark.parametrize(
    "path,params",
    [
        ("/api/v1/pnl/waterfall/PHOENIX", _PERIOD_Q),
        (
            "/api/v1/pnl/bridge/pnl.gross_margin_pct.programme.month",
            {"programme": "PHOENIX", **_BRIDGE_Q},
        ),
        ("/api/v1/pnl/pfa/PHOENIX", {"metric": "gross_pct"}),
        ("/api/v1/pnl/pyramid/PHOENIX", _PERIOD_Q),
        ("/api/v1/pnl/losses/PHOENIX", {}),
        ("/api/v1/pnl/evm/PHOENIX", _PERIOD_Q),
        ("/api/v1/pnl/dso/PHOENIX", _PERIOD_Q),
        ("/api/v1/pnl/revenue/PHOENIX", _PERIOD_Q),
        (
            "/api/v1/pnl/lineage/pnl.gross_margin_pct.programme.month",
            {"programme": "PHOENIX"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_every_endpoint_echoes_filters_applied(
    app_client: AsyncClient,
    session: AsyncSession,
    path: str,
    params: dict,
) -> None:
    await seed_novatech_m4(session)
    body = await _get(app_client, path, params)
    assert "filters_applied" in body
    fa = body["filters_applied"]
    assert isinstance(fa, dict)
    # filters_applied mirrors query-string filters. Path params do not
    # populate it, so only assert the programme echo when the caller
    # actually put ?programme= on the URL.
    if "programme" in params:
        assert fa.get("programme"), f"{path}: filters_applied.programme was empty"
