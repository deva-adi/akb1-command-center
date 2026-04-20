from __future__ import annotations

import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.models import TABLE_COUNT, Base


@pytest.mark.asyncio
async def test_metadata_has_expected_table_count(session: AsyncSession) -> None:
    del session
    assert len(Base.metadata.tables) == TABLE_COUNT


@pytest.mark.asyncio
async def test_all_metadata_tables_are_created(tmp_db_url: str) -> None:
    engine = create_async_engine(tmp_db_url, future=True)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            tables = await conn.run_sync(lambda c: set(inspect(c).get_table_names()))
    finally:
        await engine.dispose()
    assert set(Base.metadata.tables.keys()).issubset(tables)
