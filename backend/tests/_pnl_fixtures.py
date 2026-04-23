"""Shared M4 seed helpers for P&L reconciliation tests.

Leading underscore keeps pytest from collecting this file as a test
module. The helper inserts two programmes (PHOENIX lagging, ATLAS
healthy) with enough data to exercise every one of the nine active
v5.7.0 /api/v1/pnl/ endpoints. Values align with the M2 seed so
reconciliation assertions hold end to end.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CommercialScenario,
    EvmSnapshot,
    LossExposure,
    Program,
    ProgrammeRate,
    ResourcePool,
)


@dataclass(frozen=True)
class SeededProgramme:
    """Subset of the numbers the harness asserts against.

    Keeping them here lets tests read the contract as data rather than
    re-deriving it from the API response.
    """

    code: str
    program_id: int
    planned_revenue: float
    actual_revenue: float
    gross_margin_pct: float
    contribution_margin_pct: float
    portfolio_margin_pct: float
    net_margin_pct: float
    billing_ratio: float
    billed_revenue: float
    collected_revenue: float
    unbilled_wip: float
    ar_balance: float


async def seed_novatech_m4(session: AsyncSession) -> dict[str, SeededProgramme]:
    """Seed Phoenix and Atlas for cross-endpoint reconciliation tests.

    Returns a dict keyed by programme code so assertions can name the
    expected values directly.
    """
    phoenix = Program(name="Phoenix", code="PHOENIX", start_date=date(2025, 4, 1))
    atlas = Program(name="Atlas", code="ATLAS", start_date=date(2025, 4, 1))
    session.add(phoenix)
    session.add(atlas)
    await session.flush()

    # --- Phoenix ------------------------------------------------------
    phoenix_feb = CommercialScenario(
        program_id=phoenix.id,
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
    )
    phoenix_mar = CommercialScenario(
        program_id=phoenix.id,
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
    )
    session.add_all([phoenix_feb, phoenix_mar])

    # Feb and Mar tier rates for Phoenix (used by the bridge decomposition).
    for snap, weights in (
        (date(2026, 2, 1), [("Junior", 70.0, 71.0, 0.30, 0.40), ("Mid", 110.0, 114.0, 0.50, 0.415), ("Senior", 180.0, 177.5, 0.20, 0.185)]),
        (date(2026, 3, 1), [("Junior", 70.0, 72.0, 0.30, 0.50), ("Mid", 110.0, 118.0, 0.50, 0.33), ("Senior", 180.0, 175.0, 0.20, 0.17)]),
    ):
        for tier, pr, ar, pw, aw in weights:
            session.add(
                ProgrammeRate(
                    program_code="PHOENIX",
                    snapshot_date=snap,
                    role_tier=tier,
                    planned_rate=pr,
                    actual_rate=ar,
                    planned_headcount=3 if tier == "Junior" else (2 if tier == "Mid" else 1),
                    actual_headcount=3 if tier == "Junior" else (2 if tier == "Mid" else 1),
                    tier_weight_planned=pw,
                    tier_weight_actual=aw,
                )
            )

    session.add(
        EvmSnapshot(
            program_id=phoenix.id,
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

    session.add_all(
        [
            LossExposure(
                program_id=phoenix.id,
                snapshot_date=date(2026, 3, 1),
                loss_category="Bench Tax",
                amount=765_000,
                mitigation_status="Monitoring",
            ),
            LossExposure(
                program_id=phoenix.id,
                snapshot_date=date(2026, 3, 1),
                loss_category="Scope Creep",
                amount=420_000,
                mitigation_status="In Progress",
            ),
        ]
    )

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
                current_program_id=phoenix.id,
                utilization_pct=util,
                status="Active",
            )
        )

    # --- Atlas --------------------------------------------------------
    # Healthy programme: billing_ratio 0.97, collection_ratio 0.92.
    atlas_feb = CommercialScenario(
        program_id=atlas.id,
        scenario_name="Monthly Actuals",
        snapshot_date=date(2026, 2, 1),
        planned_revenue=1_100_000,
        actual_revenue=1_095_000,
        planned_cost=640_000,
        actual_cost=634_000,
        gross_margin_pct=0.421,
        contribution_margin_pct=0.285,
        portfolio_margin_pct=0.195,
        net_margin_pct=0.112,
        billing_ratio=0.97,
        billed_revenue=1_062_150,
        collected_revenue=977_178,
        unbilled_wip=32_850,
        ar_balance=84_972,
    )
    atlas_mar_billed = round(1_080_000 * 0.97)
    atlas_mar_collected = round(atlas_mar_billed * 0.92)
    atlas_mar = CommercialScenario(
        program_id=atlas.id,
        scenario_name="Monthly Actuals",
        snapshot_date=date(2026, 3, 1),
        planned_revenue=1_100_000,
        actual_revenue=1_080_000,
        planned_cost=650_000,
        actual_cost=650_000,
        gross_margin_pct=0.398,
        contribution_margin_pct=0.262,
        portfolio_margin_pct=0.178,
        net_margin_pct=0.098,
        billing_ratio=0.97,
        billed_revenue=atlas_mar_billed,
        collected_revenue=atlas_mar_collected,
        unbilled_wip=1_080_000 - atlas_mar_billed,
        ar_balance=atlas_mar_billed - atlas_mar_collected,
    )
    session.add_all([atlas_feb, atlas_mar])

    for snap, weights in (
        (date(2026, 2, 1), [("Junior", 70.0, 70.0, 0.30, 0.30), ("Mid", 110.0, 110.0, 0.50, 0.50), ("Senior", 180.0, 180.0, 0.20, 0.20)]),
        (date(2026, 3, 1), [("Junior", 70.0, 70.0, 0.30, 0.30), ("Mid", 110.0, 115.0, 0.50, 0.50), ("Senior", 180.0, 180.0, 0.20, 0.20)]),
    ):
        for tier, pr, ar, pw, aw in weights:
            session.add(
                ProgrammeRate(
                    program_code="ATLAS",
                    snapshot_date=snap,
                    role_tier=tier,
                    planned_rate=pr,
                    actual_rate=ar,
                    planned_headcount=3 if tier == "Junior" else (5 if tier == "Mid" else 2),
                    actual_headcount=3 if tier == "Junior" else (5 if tier == "Mid" else 2),
                    tier_weight_planned=pw,
                    tier_weight_actual=aw,
                )
            )

    session.add(
        EvmSnapshot(
            program_id=atlas.id,
            snapshot_date=date(2026, 3, 1),
            planned_value=700_000,
            earned_value=710_000,
            actual_cost=680_000,
            bac=8_500_000,
            cpi=1.044,
            spi=1.014,
            eac=8_140_000,
            tcpi=0.96,
            vac=360_000,
            percent_complete=8.4,
        )
    )

    session.add(
        LossExposure(
            program_id=atlas.id,
            snapshot_date=date(2026, 3, 1),
            loss_category="Rate Drift",
            amount=95_000,
            mitigation_status="In Progress",
        )
    )

    for name, tier, util in [
        ("Gaurav Mehta", "Senior", 90.0),
        ("Neha Kapoor", "Senior", 92.0),
        ("Siddharth Jain", "Mid", 88.0),
        ("Pooja Verma", "Mid", 86.0),
        ("Rahul Iyer", "Mid", 87.0),
    ]:
        session.add(
            ResourcePool(
                name=name,
                role_tier=tier,
                current_program_id=atlas.id,
                utilization_pct=util,
                status="Active",
            )
        )

    await session.commit()

    return {
        "PHOENIX": SeededProgramme(
            code="PHOENIX",
            program_id=phoenix.id,
            planned_revenue=850_000,
            actual_revenue=820_000,
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
        "ATLAS": SeededProgramme(
            code="ATLAS",
            program_id=atlas.id,
            planned_revenue=1_100_000,
            actual_revenue=1_080_000,
            gross_margin_pct=0.398,
            contribution_margin_pct=0.262,
            portfolio_margin_pct=0.178,
            net_margin_pct=0.098,
            billing_ratio=0.97,
            billed_revenue=atlas_mar_billed,
            collected_revenue=atlas_mar_collected,
            unbilled_wip=1_080_000 - atlas_mar_billed,
            ar_balance=atlas_mar_billed - atlas_mar_collected,
        ),
    }
