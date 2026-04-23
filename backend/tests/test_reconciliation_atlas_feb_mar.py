"""PRD section 6.2 reconciliation test for Atlas Feb to Mar 2026.

Per PRD worked example:
    Prior 42.1 percent, current 39.8 percent, delta minus 230 basis points.

This test asserts the total gross_margin_pct delta on the seeded values
reconciles to minus 230 bps within 1 bp tolerance. Same contract as the
Phoenix test; this is the second hard-rule-8 gate.
"""
from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommercialScenario, Program
from app.seed.pnl_seed import seed_monthly_actuals_2026_feb_mar


@pytest.mark.asyncio
async def test_atlas_feb_to_mar_gross_margin_delta_is_minus_230_bps(
    session: AsyncSession,
) -> None:
    p = Program(name="Atlas", code="ATLAS", start_date=date(2025, 4, 1))
    session.add(p)
    await session.flush()
    await session.commit()

    await seed_monthly_actuals_2026_feb_mar(session, {"ATLAS": p.id})
    await session.commit()

    stmt = (
        select(CommercialScenario.snapshot_date, CommercialScenario.gross_margin_pct)
        .where(CommercialScenario.program_id == p.id)
        .where(CommercialScenario.scenario_name == "Monthly Actuals")
        .where(CommercialScenario.snapshot_date.in_([date(2026, 2, 1), date(2026, 3, 1)]))
    )
    rows = {row[0]: row[1] for row in (await session.execute(stmt)).all()}

    feb_gross = rows[date(2026, 2, 1)]
    mar_gross = rows[date(2026, 3, 1)]

    delta_bps = (mar_gross - feb_gross) * 10000

    assert abs(delta_bps - (-230.0)) < 1.0, (
        f"Atlas Feb to Mar gross margin delta is {delta_bps:.2f} bps, "
        f"expected -230.00 bps within 1 bp tolerance. "
        f"Feb gross={feb_gross:.4f}, Mar gross={mar_gross:.4f}."
    )
