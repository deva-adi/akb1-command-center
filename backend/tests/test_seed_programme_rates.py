"""Tests for the programme_rates seed (M2, piece 1)."""
from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Program, ProgrammeRate
from app.seed.pnl_seed import seed_programme_rates


async def _insert_programmes(session: AsyncSession) -> dict[str, int]:
    """Add the seven expected programmes directly so the seed can key on them."""
    codes = ["PHOENIX", "ATLAS", "SENTINEL", "ORION", "TITAN", "HERCULES", "BHARAT"]
    ids: dict[str, int] = {}
    for code in codes:
        p = Program(name=code.title(), code=code, start_date=date(2025, 4, 1))
        session.add(p)
        await session.flush()
        ids[code] = p.id
    await session.commit()
    return ids


@pytest.mark.asyncio
async def test_programme_rates_seed_inserts_exactly_252_rows(session: AsyncSession) -> None:
    ids = await _insert_programmes(session)

    result = await seed_programme_rates(session, programme_codes=ids.keys())
    await session.commit()

    assert result["inserted"] == 252
    assert result["skipped"] == 0

    total = (await session.execute(select(func.count(ProgrammeRate.id)))).scalar_one()
    assert total == 252


@pytest.mark.asyncio
async def test_programme_rates_tuples_are_unique(session: AsyncSession) -> None:
    ids = await _insert_programmes(session)
    await seed_programme_rates(session, programme_codes=ids.keys())
    await session.commit()

    # Each (program_code, snapshot_date, role_tier) must be unique.
    stmt = (
        select(ProgrammeRate.program_code, ProgrammeRate.snapshot_date, ProgrammeRate.role_tier, func.count(ProgrammeRate.id))
        .group_by(ProgrammeRate.program_code, ProgrammeRate.snapshot_date, ProgrammeRate.role_tier)
    )
    rows = (await session.execute(stmt)).all()
    assert len(rows) == 252
    for row in rows:
        assert row[3] == 1, f"duplicate tuple: {row[0]} {row[1]} {row[2]}"

    # Three tiers present per programme.
    tiers = {r[2] for r in rows}
    assert tiers == {"Junior", "Mid", "Senior"}

    # All twelve 2026 month starts present.
    months = sorted({r[1] for r in rows})
    assert months[0] == date(2026, 1, 1)
    assert months[-1] == date(2026, 12, 1)
    assert len(months) == 12


@pytest.mark.asyncio
async def test_programme_rates_seed_is_idempotent(session: AsyncSession) -> None:
    ids = await _insert_programmes(session)

    first = await seed_programme_rates(session, programme_codes=ids.keys())
    await session.commit()
    second = await seed_programme_rates(session, programme_codes=ids.keys())
    await session.commit()

    assert first["inserted"] == 252
    assert first["skipped"] == 0
    assert second["inserted"] == 0
    assert second["skipped"] == 252

    total = (await session.execute(select(func.count(ProgrammeRate.id)))).scalar_one()
    assert total == 252
