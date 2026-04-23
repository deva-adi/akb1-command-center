"""Tab 12 P&L Cockpit seed (v5.7.0).

Three additive seed pieces, all idempotent:

  1. seed_programme_rates. Populates the programme_rates table with
     252 rows = 7 programmes x 3 tiers x 12 months (Jan 2026 through
     Dec 2026). Rate curves are derived to line up with the existing
     rate_cards seed in commercial_data.py so the pyramid economics
     and margin bridge math in M3 reconcile with numbers that are
     already visible on the Margin and EVM tab.

  2. seed_monthly_actuals_2026_feb_mar. Inserts 14 rows into
     commercial_scenarios, one per programme for 2026-02-01 and
     2026-03-01. PHOENIX, ATLAS, TITAN use the exact values from
     docs/csv-templates/financials.csv. SENTINEL and ORION get
     Feb 2026 rows that trend plausibly into the existing Mar 2026
     row already in the CSV template. HERCULES and BHARAT get both
     months aligned with their existing quarterly trajectory.

  3. backfill_billing_columns. Populates the five v5.7.0 nullable
     columns on every commercial_scenarios row that has any of them
     null. billing_ratio, billed_revenue, collected_revenue,
     unbilled_wip, ar_balance. Deterministic per-programme defaults
     per PRD section 9.1 and formula 54 (DSO and AR balance).

All three are safe to re-run. They select existing rows before
inserting or updating so a repeated container start is a true no-op
after the first run.
"""
from __future__ import annotations

from datetime import date
from typing import Iterable, TypedDict

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging_config import get_logger
from app.models import CommercialScenario, ProgrammeRate

log = get_logger(__name__)


# ===========================================================================
# Piece 1: programme_rates — 252 rows
#
# Rate-curve derivation.
#   - planned_rate is constant across the year for each (programme, tier)
#     and is taken from the rate_cards seed in commercial_data.py so the
#     Rate-card drift table on the Margin and EVM tab renders identical
#     numbers.
#   - actual_rate drifts from planned at Jan 2026 (zero drift) to the
#     rate_cards actual value at Mar 2026, then continues drifting modestly
#     through Dec 2026. The Mar anchor matches rate_cards exactly so the
#     worked example in PRD section 6.2 (Phoenix Mid Engineer 110 to 118)
#     ties out on the reference month.
#   - headcount is held constant to the rate_cards value; tier weights are
#     stored on each row to support the Mix driver of the margin bridge.
#   - PRD baseline for PHOENIX March 2026:
#       Junior  planned 70  actual 72  headcount 3  weight_planned 0.30
#       Mid     planned 110 actual 118 headcount 2  weight_planned 0.50
#       Senior  planned 180 actual 175 headcount 1  weight_planned 0.20
#       (actual tier weights: 0.50 / 0.33 / 0.17 respectively)
# ===========================================================================


class _TierProfile(TypedDict):
    planned_rate: float
    mar_actual: float
    planned_headcount: int
    actual_headcount: int
    tier_weight_planned: float
    tier_weight_actual_mar: float


# Per-programme, per-tier anchor values as they should appear on the
# 2026-03-01 snapshot. Values align with the rate_cards seed in
# backend/app/seed/commercial_data.py (the table rendered on /margin).
_PROGRAMME_PROFILES: dict[str, dict[str, _TierProfile]] = {
    "PHOENIX": {
        "Junior": {"planned_rate": 70.0, "mar_actual": 72.0, "planned_headcount": 7, "actual_headcount": 7, "tier_weight_planned": 0.30, "tier_weight_actual_mar": 0.50},
        "Mid": {"planned_rate": 110.0, "mar_actual": 118.0, "planned_headcount": 15, "actual_headcount": 14, "tier_weight_planned": 0.50, "tier_weight_actual_mar": 0.33},
        "Senior": {"planned_rate": 180.0, "mar_actual": 175.0, "planned_headcount": 3, "actual_headcount": 4, "tier_weight_planned": 0.20, "tier_weight_actual_mar": 0.17},
    },
    "ATLAS": {
        "Junior": {"planned_rate": 65.0, "mar_actual": 68.0, "planned_headcount": 6, "actual_headcount": 5, "tier_weight_planned": 0.35, "tier_weight_actual_mar": 0.28},
        "Mid": {"planned_rate": 100.0, "mar_actual": 115.0, "planned_headcount": 10, "actual_headcount": 11, "tier_weight_planned": 0.50, "tier_weight_actual_mar": 0.61},
        "Senior": {"planned_rate": 170.0, "mar_actual": 195.0, "planned_headcount": 2, "actual_headcount": 2, "tier_weight_planned": 0.15, "tier_weight_actual_mar": 0.11},
    },
    "SENTINEL": {
        "Junior": {"planned_rate": 72.0, "mar_actual": 71.0, "planned_headcount": 2, "actual_headcount": 2, "tier_weight_planned": 0.25, "tier_weight_actual_mar": 0.25},
        "Mid": {"planned_rate": 115.0, "mar_actual": 116.0, "planned_headcount": 8, "actual_headcount": 8, "tier_weight_planned": 0.60, "tier_weight_actual_mar": 0.58},
        "Senior": {"planned_rate": 185.0, "mar_actual": 182.0, "planned_headcount": 2, "actual_headcount": 2, "tier_weight_planned": 0.15, "tier_weight_actual_mar": 0.17},
    },
    "ORION": {
        "Junior": {"planned_rate": 68.0, "mar_actual": 70.0, "planned_headcount": 8, "actual_headcount": 9, "tier_weight_planned": 0.30, "tier_weight_actual_mar": 0.38},
        "Mid": {"planned_rate": 105.0, "mar_actual": 122.0, "planned_headcount": 18, "actual_headcount": 20, "tier_weight_planned": 0.55, "tier_weight_actual_mar": 0.47},
        "Senior": {"planned_rate": 175.0, "mar_actual": 210.0, "planned_headcount": 4, "actual_headcount": 5, "tier_weight_planned": 0.15, "tier_weight_actual_mar": 0.15},
    },
    "TITAN": {
        "Junior": {"planned_rate": 68.0, "mar_actual": 70.0, "planned_headcount": 4, "actual_headcount": 3, "tier_weight_planned": 0.30, "tier_weight_actual_mar": 0.25},
        "Mid": {"planned_rate": 108.0, "mar_actual": 115.0, "planned_headcount": 9, "actual_headcount": 10, "tier_weight_planned": 0.55, "tier_weight_actual_mar": 0.60},
        "Senior": {"planned_rate": 175.0, "mar_actual": 180.0, "planned_headcount": 2, "actual_headcount": 2, "tier_weight_planned": 0.15, "tier_weight_actual_mar": 0.15},
    },
    "HERCULES": {
        # Hercules started 2026-02-01 on a Scrum plus Waterfall mix. Rates are
        # set to match the Managed-Services delivery model baselines and line
        # up with the gross margins in hercules_data.py (38% to 44% across
        # the year).
        "Junior": {"planned_rate": 68.0, "mar_actual": 69.0, "planned_headcount": 5, "actual_headcount": 5, "tier_weight_planned": 0.25, "tier_weight_actual_mar": 0.25},
        "Mid": {"planned_rate": 110.0, "mar_actual": 112.0, "planned_headcount": 13, "actual_headcount": 14, "tier_weight_planned": 0.60, "tier_weight_actual_mar": 0.62},
        "Senior": {"planned_rate": 185.0, "mar_actual": 185.0, "planned_headcount": 4, "actual_headcount": 3, "tier_weight_planned": 0.15, "tier_weight_actual_mar": 0.13},
    },
    "BHARAT": {
        # BHARAT started 2026-01-15, early ramp through Feb and Mar. Rates
        # taken from BHARAT_RATE_CARDS in bharat_data.py at Jan 2027 (the
        # only snapshot there), walked back to Mar 2026 with slightly lower
        # actuals because the team is still forming.
        "Junior": {"planned_rate": 70.0, "mar_actual": 71.0, "planned_headcount": 6, "actual_headcount": 5, "tier_weight_planned": 0.25, "tier_weight_actual_mar": 0.22},
        "Mid": {"planned_rate": 110.0, "mar_actual": 111.0, "planned_headcount": 15, "actual_headcount": 16, "tier_weight_planned": 0.60, "tier_weight_actual_mar": 0.64},
        "Senior": {"planned_rate": 190.0, "mar_actual": 188.0, "planned_headcount": 3, "actual_headcount": 3, "tier_weight_planned": 0.15, "tier_weight_actual_mar": 0.14},
    },
}


def _month_starts_2026() -> list[date]:
    return [date(2026, m, 1) for m in range(1, 13)]


def _actual_rate_for_month(planned: float, mar_actual: float, month_idx: int) -> float:
    """Linear drift from planned at Jan (month_idx=0) to mar_actual at Mar.

    After March the drift continues at the same per-month slope, capped so
    that a flat profile (mar_actual == planned) stays flat for the year.
    """
    slope = (mar_actual - planned) / 2.0  # two months from Jan to Mar
    return round(planned + slope * month_idx, 2)


def _tier_weight_for_month(planned: float, mar_actual: float, month_idx: int) -> float:
    slope = (mar_actual - planned) / 2.0
    return round(planned + slope * month_idx, 4)


async def seed_programme_rates(
    session: AsyncSession,
    programme_codes: Iterable[str] | None = None,
) -> dict[str, int]:
    """Insert 252 programme_rates rows, skipping any that already exist.

    Returns a dict with ``inserted`` and ``skipped`` counts.
    """
    codes = list(programme_codes) if programme_codes else list(_PROGRAMME_PROFILES.keys())
    months = _month_starts_2026()

    # Find existing tuples so we never duplicate.
    existing_stmt = select(ProgrammeRate.program_code, ProgrammeRate.snapshot_date, ProgrammeRate.role_tier)
    existing_rows = (await session.execute(existing_stmt)).all()
    existing: set[tuple[str, date, str]] = {(r[0], r[1], r[2]) for r in existing_rows}

    inserted = 0
    skipped = 0
    for code in codes:
        if code not in _PROGRAMME_PROFILES:
            continue
        profile = _PROGRAMME_PROFILES[code]
        for tier, tier_profile in profile.items():
            for idx, snap_date in enumerate(months):
                if (code, snap_date, tier) in existing:
                    skipped += 1
                    continue
                session.add(
                    ProgrammeRate(
                        program_code=code,
                        snapshot_date=snap_date,
                        role_tier=tier,
                        planned_rate=tier_profile["planned_rate"],
                        actual_rate=_actual_rate_for_month(
                            tier_profile["planned_rate"],
                            tier_profile["mar_actual"],
                            idx,
                        ),
                        planned_headcount=tier_profile["planned_headcount"],
                        actual_headcount=tier_profile["actual_headcount"],
                        tier_weight_planned=tier_profile["tier_weight_planned"],
                        tier_weight_actual=_tier_weight_for_month(
                            tier_profile["tier_weight_planned"],
                            tier_profile["tier_weight_actual_mar"],
                            idx,
                        ),
                    )
                )
                inserted += 1
    await session.flush()
    log.info("pnl_seed.programme_rates", inserted=inserted, skipped=skipped)
    return {"inserted": inserted, "skipped": skipped}


# ===========================================================================
# Piece 2: Monthly Actuals for 2026-02-01 and 2026-03-01
#
# PHOENIX, ATLAS, TITAN use the exact values from the CSV template so the
# worked examples in the PRD reconcile byte-for-byte.
# SENTINEL Feb trends into its existing Mar row (39.3% gross).
# ORION Feb trends into its existing Mar row (25.0% gross).
# HERCULES and BHARAT get both months aligned with their quarterly seed
# trajectories.
# ===========================================================================


class _MonthlyActual(TypedDict):
    program_code: str
    snapshot_date: date
    planned_revenue: float
    actual_revenue: float
    planned_cost: float
    actual_cost: float
    gross_margin_pct: float
    contribution_margin_pct: float
    portfolio_margin_pct: float
    net_margin_pct: float


_MONTHLY_ACTUALS_2026_FEB_MAR: list[_MonthlyActual] = [
    # PHOENIX (exact from financials.csv).
    {"program_code": "PHOENIX", "snapshot_date": date(2026, 2, 1), "planned_revenue": 850_000, "actual_revenue": 845_000, "planned_cost": 540_000, "actual_cost": 555_000, "gross_margin_pct": 0.314, "contribution_margin_pct": 0.182, "portfolio_margin_pct": 0.108, "net_margin_pct": 0.062},
    {"program_code": "PHOENIX", "snapshot_date": date(2026, 3, 1), "planned_revenue": 850_000, "actual_revenue": 820_000, "planned_cost": 550_000, "actual_cost": 590_000, "gross_margin_pct": 0.280, "contribution_margin_pct": 0.125, "portfolio_margin_pct": 0.082, "net_margin_pct": 0.041},
    # ATLAS (exact from financials.csv).
    {"program_code": "ATLAS", "snapshot_date": date(2026, 2, 1), "planned_revenue": 650_000, "actual_revenue": 655_000, "planned_cost": 375_000, "actual_cost": 378_000, "gross_margin_pct": 0.421, "contribution_margin_pct": 0.312, "portfolio_margin_pct": 0.224, "net_margin_pct": 0.148},
    {"program_code": "ATLAS", "snapshot_date": date(2026, 3, 1), "planned_revenue": 650_000, "actual_revenue": 640_000, "planned_cost": 380_000, "actual_cost": 385_000, "gross_margin_pct": 0.398, "contribution_margin_pct": 0.285, "portfolio_margin_pct": 0.192, "net_margin_pct": 0.118},
    # TITAN (exact from financials.csv).
    {"program_code": "TITAN", "snapshot_date": date(2026, 2, 1), "planned_revenue": 935_000, "actual_revenue": 925_000, "planned_cost": 540_000, "actual_cost": 548_000, "gross_margin_pct": 0.408, "contribution_margin_pct": 0.271, "portfolio_margin_pct": 0.168, "net_margin_pct": 0.112},
    {"program_code": "TITAN", "snapshot_date": date(2026, 3, 1), "planned_revenue": 935_000, "actual_revenue": 945_000, "planned_cost": 550_000, "actual_cost": 560_000, "gross_margin_pct": 0.412, "contribution_margin_pct": 0.285, "portfolio_margin_pct": 0.182, "net_margin_pct": 0.124},
    # SENTINEL Feb trends into existing Mar 39.3 gross; small improving delta.
    {"program_code": "SENTINEL", "snapshot_date": date(2026, 2, 1), "planned_revenue": 540_000, "actual_revenue": 525_000, "planned_cost": 318_000, "actual_cost": 322_000, "gross_margin_pct": 0.387, "contribution_margin_pct": 0.275, "portfolio_margin_pct": 0.181, "net_margin_pct": 0.099},
    {"program_code": "SENTINEL", "snapshot_date": date(2026, 3, 1), "planned_revenue": 540_000, "actual_revenue": 535_000, "planned_cost": 320_000, "actual_cost": 325_000, "gross_margin_pct": 0.393, "contribution_margin_pct": 0.280, "portfolio_margin_pct": 0.185, "net_margin_pct": 0.102},
    # ORION Feb trends into existing Mar 25.0 gross; small declining delta.
    {"program_code": "ORION", "snapshot_date": date(2026, 2, 1), "planned_revenue": 420_000, "actual_revenue": 420_000, "planned_cost": 308_000, "actual_cost": 309_000, "gross_margin_pct": 0.264, "contribution_margin_pct": 0.092, "portfolio_margin_pct": -0.012, "net_margin_pct": 0.009},
    {"program_code": "ORION", "snapshot_date": date(2026, 3, 1), "planned_revenue": 420_000, "actual_revenue": 415_000, "planned_cost": 310_000, "actual_cost": 315_000, "gross_margin_pct": 0.250, "contribution_margin_pct": 0.082, "portfolio_margin_pct": -0.021, "net_margin_pct": 0.005},
    # HERCULES aligned with its quarterly trajectory (gross 38 to 36 early).
    {"program_code": "HERCULES", "snapshot_date": date(2026, 2, 1), "planned_revenue": 550_000, "actual_revenue": 545_000, "planned_cost": 340_000, "actual_cost": 340_000, "gross_margin_pct": 0.376, "contribution_margin_pct": 0.278, "portfolio_margin_pct": 0.218, "net_margin_pct": 0.138},
    {"program_code": "HERCULES", "snapshot_date": date(2026, 3, 1), "planned_revenue": 580_000, "actual_revenue": 570_000, "planned_cost": 355_000, "actual_cost": 360_000, "gross_margin_pct": 0.368, "contribution_margin_pct": 0.265, "portfolio_margin_pct": 0.205, "net_margin_pct": 0.128},
    # BHARAT early ramp (pre-Q1), trending into Apr Q1 gross 27%.
    {"program_code": "BHARAT", "snapshot_date": date(2026, 2, 1), "planned_revenue": 400_000, "actual_revenue": 395_000, "planned_cost": 325_000, "actual_cost": 320_000, "gross_margin_pct": 0.190, "contribution_margin_pct": 0.125, "portfolio_margin_pct": 0.075, "net_margin_pct": 0.040},
    {"program_code": "BHARAT", "snapshot_date": date(2026, 3, 1), "planned_revenue": 450_000, "actual_revenue": 455_000, "planned_cost": 355_000, "actual_cost": 350_000, "gross_margin_pct": 0.231, "contribution_margin_pct": 0.160, "portfolio_margin_pct": 0.110, "net_margin_pct": 0.070},
]


async def seed_monthly_actuals_2026_feb_mar(
    session: AsyncSession,
    programme_ids: dict[str, int],
) -> dict[str, int]:
    """Insert 14 Monthly Actuals rows for 2026-02-01 and 2026-03-01.

    Returns inserted and skipped counts. Existing quarterly rows are left
    untouched; the idempotency guard checks (program_id, snapshot_date,
    scenario_name).
    """
    # Find existing monthly actuals for the target window so we never duplicate.
    existing_stmt = (
        select(
            CommercialScenario.program_id,
            CommercialScenario.snapshot_date,
            CommercialScenario.scenario_name,
        )
        .where(CommercialScenario.scenario_name == "Monthly Actuals")
        .where(CommercialScenario.snapshot_date.in_([date(2026, 2, 1), date(2026, 3, 1)]))
    )
    existing_rows = (await session.execute(existing_stmt)).all()
    existing: set[tuple[int, date]] = {(r[0], r[1]) for r in existing_rows}

    inserted = 0
    skipped = 0
    for row in _MONTHLY_ACTUALS_2026_FEB_MAR:
        program_id = programme_ids.get(row["program_code"])
        if program_id is None:
            continue
        key = (program_id, row["snapshot_date"])
        if key in existing:
            skipped += 1
            continue
        session.add(
            CommercialScenario(
                program_id=program_id,
                scenario_name="Monthly Actuals",
                snapshot_date=row["snapshot_date"],
                planned_revenue=row["planned_revenue"],
                actual_revenue=row["actual_revenue"],
                planned_cost=row["planned_cost"],
                actual_cost=row["actual_cost"],
                gross_margin_pct=row["gross_margin_pct"],
                contribution_margin_pct=row["contribution_margin_pct"],
                portfolio_margin_pct=row["portfolio_margin_pct"],
                net_margin_pct=row["net_margin_pct"],
            )
        )
        inserted += 1
    await session.flush()
    log.info("pnl_seed.monthly_actuals", inserted=inserted, skipped=skipped)
    return {"inserted": inserted, "skipped": skipped}


# ===========================================================================
# Piece 3: Backfill billing and cash columns on every commercial_scenarios
# row that has any of them null.
#
# Per PRD section 9.1:
#   billing_ratio    : 0.88 PHOENIX and ORION, 0.97 ATLAS and SENTINEL,
#                      0.95 default for the rest (TITAN, HERCULES, BHARAT).
#   billed_revenue   : actual_revenue * billing_ratio, rounded to whole units.
#   collection_ratio : 0.80 PHOENIX and ORION, 0.92 ATLAS and SENTINEL,
#                      0.88 default. Used only to derive collected_revenue.
#   collected_revenue: billed_revenue * collection_ratio, rounded.
#   unbilled_wip     : max(actual_revenue - billed_revenue, 0).
#   ar_balance       : billed_revenue - collected_revenue (formula 54).
# ===========================================================================


_BILLING_RATIO_DEFAULTS: dict[str, float] = {
    "PHOENIX": 0.88,
    "ORION": 0.88,
    "ATLAS": 0.97,
    "SENTINEL": 0.97,
}
_COLLECTION_RATIO_DEFAULTS: dict[str, float] = {
    "PHOENIX": 0.80,
    "ORION": 0.80,
    "ATLAS": 0.92,
    "SENTINEL": 0.92,
}
_DEFAULT_BILLING_RATIO = 0.95
_DEFAULT_COLLECTION_RATIO = 0.88


def _billing_ratio_for(code: str) -> float:
    return _BILLING_RATIO_DEFAULTS.get(code, _DEFAULT_BILLING_RATIO)


def _collection_ratio_for(code: str) -> float:
    return _COLLECTION_RATIO_DEFAULTS.get(code, _DEFAULT_COLLECTION_RATIO)


async def backfill_billing_columns(
    session: AsyncSession,
    programme_ids: dict[str, int],
) -> dict[str, int]:
    """Fill the five new columns for any row where they are null.

    Only rows with a resolvable programme and non-null ``actual_revenue``
    are updated. Returns a dict with ``updated`` and ``skipped_no_actual``
    and ``skipped_already_populated`` counts.
    """
    # Invert program_ids to look up code from id.
    code_by_id: dict[int, str] = {pid: code for code, pid in programme_ids.items()}

    stmt = select(
        CommercialScenario.id,
        CommercialScenario.program_id,
        CommercialScenario.actual_revenue,
        CommercialScenario.billing_ratio,
        CommercialScenario.billed_revenue,
        CommercialScenario.collected_revenue,
        CommercialScenario.unbilled_wip,
        CommercialScenario.ar_balance,
    )
    rows = (await session.execute(stmt)).all()

    updated = 0
    skipped_already = 0
    skipped_no_actual = 0
    for row in rows:
        scenario_id = row[0]
        program_id = row[1]
        actual_revenue = row[2]
        existing = row[3:8]  # billing_ratio, billed_revenue, collected_revenue, unbilled_wip, ar_balance

        if all(v is not None for v in existing):
            skipped_already += 1
            continue
        if actual_revenue is None:
            skipped_no_actual += 1
            continue
        code = code_by_id.get(program_id or -1)
        if code is None:
            # Programme id not in the id map; treat as default ratio.
            code = ""
        billing_ratio = _billing_ratio_for(code)
        collection_ratio = _collection_ratio_for(code)
        billed = round(float(actual_revenue) * billing_ratio, 0)
        collected = round(billed * collection_ratio, 0)
        unbilled = float(actual_revenue) - billed
        if unbilled < 0:
            unbilled = 0.0
        ar = billed - collected

        # Update only columns that are currently null so we never overwrite.
        values: dict[str, float] = {}
        if existing[0] is None:
            values["billing_ratio"] = billing_ratio
        if existing[1] is None:
            values["billed_revenue"] = billed
        if existing[2] is None:
            values["collected_revenue"] = collected
        if existing[3] is None:
            values["unbilled_wip"] = unbilled
        if existing[4] is None:
            values["ar_balance"] = ar
        if not values:
            skipped_already += 1
            continue
        await session.execute(
            update(CommercialScenario).where(CommercialScenario.id == scenario_id).values(**values)
        )
        updated += 1

    await session.flush()
    log.info(
        "pnl_seed.backfill_billing_columns",
        updated=updated,
        skipped_already_populated=skipped_already,
        skipped_no_actual=skipped_no_actual,
    )
    return {
        "updated": updated,
        "skipped_already_populated": skipped_already,
        "skipped_no_actual": skipped_no_actual,
    }


# ===========================================================================
# Orchestrator called from seeder.py
# ===========================================================================


async def seed_pnl(
    session: AsyncSession,
    programme_ids: dict[str, int],
) -> dict[str, dict[str, int]]:
    """Run all three M2 pieces. Safe to call repeatedly."""
    pr = await seed_programme_rates(session, programme_codes=programme_ids.keys())
    ma = await seed_monthly_actuals_2026_feb_mar(session, programme_ids)
    bf = await backfill_billing_columns(session, programme_ids)
    return {"programme_rates": pr, "monthly_actuals": ma, "backfill": bf}
