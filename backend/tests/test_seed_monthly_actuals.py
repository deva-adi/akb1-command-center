"""Tests for the Feb-Mar 2026 Monthly Actuals seed (M2, piece 2)."""
from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommercialScenario, Program
from app.seed.pnl_seed import seed_monthly_actuals_2026_feb_mar


async def _insert_programmes_and_quarterly(session: AsyncSession) -> dict[str, int]:
    """Seed programmes plus one quarterly commercial_scenarios row per programme.

    The quarterly rows let the idempotency test verify that existing non-
    Monthly-Actuals rows are untouched by the monthly seed.
    """
    codes = ["PHOENIX", "ATLAS", "SENTINEL", "ORION", "TITAN", "HERCULES", "BHARAT"]
    ids: dict[str, int] = {}
    for code in codes:
        p = Program(name=code.title(), code=code, start_date=date(2025, 4, 1))
        session.add(p)
        await session.flush()
        ids[code] = p.id
        # A quarterly anchor row that the seed must leave alone.
        session.add(
            CommercialScenario(
                program_id=p.id,
                scenario_name="Quarterly Actuals",
                snapshot_date=date(2026, 1, 1),
                planned_revenue=1_000_000,
                actual_revenue=1_010_000,
                planned_cost=700_000,
                actual_cost=710_000,
                gross_margin_pct=0.30,
            )
        )
    await session.commit()
    return ids


@pytest.mark.asyncio
async def test_monthly_actuals_seed_inserts_exactly_14_rows(session: AsyncSession) -> None:
    ids = await _insert_programmes_and_quarterly(session)

    result = await seed_monthly_actuals_2026_feb_mar(session, ids)
    await session.commit()

    assert result["inserted"] == 14
    assert result["skipped"] == 0

    count = (
        await session.execute(
            select(func.count(CommercialScenario.id))
            .where(CommercialScenario.scenario_name == "Monthly Actuals")
            .where(CommercialScenario.snapshot_date.in_([date(2026, 2, 1), date(2026, 3, 1)]))
        )
    ).scalar_one()
    assert count == 14


@pytest.mark.asyncio
async def test_monthly_actuals_scenario_name_is_exact(session: AsyncSession) -> None:
    ids = await _insert_programmes_and_quarterly(session)
    await seed_monthly_actuals_2026_feb_mar(session, ids)
    await session.commit()

    stmt = (
        select(CommercialScenario.scenario_name)
        .where(CommercialScenario.snapshot_date.in_([date(2026, 2, 1), date(2026, 3, 1)]))
        .where(CommercialScenario.program_id.in_(list(ids.values())))
    )
    names = [row[0] for row in (await session.execute(stmt)).all()]
    assert len(names) == 14
    assert all(n == "Monthly Actuals" for n in names)


@pytest.mark.asyncio
async def test_monthly_actuals_seed_is_idempotent(session: AsyncSession) -> None:
    ids = await _insert_programmes_and_quarterly(session)

    first = await seed_monthly_actuals_2026_feb_mar(session, ids)
    await session.commit()
    second = await seed_monthly_actuals_2026_feb_mar(session, ids)
    await session.commit()

    assert first["inserted"] == 14
    assert first["skipped"] == 0
    assert second["inserted"] == 0
    assert second["skipped"] == 14


@pytest.mark.asyncio
async def test_monthly_actuals_seed_leaves_existing_quarterly_untouched(
    session: AsyncSession,
) -> None:
    ids = await _insert_programmes_and_quarterly(session)

    # Snapshot quarterly rows before the seed runs.
    quarterly_before = (
        await session.execute(
            select(CommercialScenario.id, CommercialScenario.gross_margin_pct)
            .where(CommercialScenario.scenario_name == "Quarterly Actuals")
        )
    ).all()

    await seed_monthly_actuals_2026_feb_mar(session, ids)
    await session.commit()

    # Re-read and verify each quarterly row is byte-identical.
    quarterly_after = (
        await session.execute(
            select(CommercialScenario.id, CommercialScenario.gross_margin_pct)
            .where(CommercialScenario.scenario_name == "Quarterly Actuals")
        )
    ).all()

    assert len(quarterly_before) == len(quarterly_after) == 7
    before_map = {row[0]: row[1] for row in quarterly_before}
    after_map = {row[0]: row[1] for row in quarterly_after}
    assert before_map == after_map
