"""PRD section 6.2 reconciliation test for Phoenix Feb to Mar 2026.

Per PRD worked example:
    Prior month gross margin 31.4 percent, current month 28.0 percent,
    delta minus 340 basis points.

The Margin Bridge in PRD section 6.2 is a gross-margin bridge. This test
asserts the total gross_margin_pct delta on the seeded values reconciles
to minus 340 bps within 1 bp tolerance. The Price, Volume, Mix, Cost
decomposition is evaluated in later M3 endpoint tests; this test is the
hard-rule-8 gate on the seed itself.
"""
from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommercialScenario, Program
from app.seed.pnl_seed import seed_monthly_actuals_2026_feb_mar


@pytest.mark.asyncio
async def test_phoenix_feb_to_mar_gross_margin_delta_is_minus_340_bps(
    session: AsyncSession,
) -> None:
    # Insert just the programme we need.
    p = Program(name="Phoenix", code="PHOENIX", start_date=date(2025, 4, 1))
    session.add(p)
    await session.flush()
    await session.commit()

    await seed_monthly_actuals_2026_feb_mar(session, {"PHOENIX": p.id})
    await session.commit()

    # Pull Feb and Mar Monthly Actuals rows straight from the DB.
    stmt = (
        select(CommercialScenario.snapshot_date, CommercialScenario.gross_margin_pct)
        .where(CommercialScenario.program_id == p.id)
        .where(CommercialScenario.scenario_name == "Monthly Actuals")
        .where(CommercialScenario.snapshot_date.in_([date(2026, 2, 1), date(2026, 3, 1)]))
    )
    rows = {row[0]: row[1] for row in (await session.execute(stmt)).all()}

    feb_gross = rows[date(2026, 2, 1)]
    mar_gross = rows[date(2026, 3, 1)]

    # gross_margin_pct is stored as a decimal fraction (0.314 = 31.4%).
    # Delta in basis points = (mar - feb) * 10000.
    delta_bps = (mar_gross - feb_gross) * 10000

    assert abs(delta_bps - (-340.0)) < 1.0, (
        f"Phoenix Feb to Mar gross margin delta is {delta_bps:.2f} bps, "
        f"expected -340.00 bps within 1 bp tolerance. "
        f"Feb gross={feb_gross:.4f}, Mar gross={mar_gross:.4f}."
    )
