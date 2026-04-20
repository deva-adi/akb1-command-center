from __future__ import annotations

import asyncio
import os
import sys
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.database import reset_engine_for_tests
from app.models import Base


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def tmp_db_url(tmp_path_factory: pytest.TempPathFactory) -> AsyncIterator[str]:
    tmp_dir = tmp_path_factory.mktemp("akb1-db")
    db_path = tmp_dir / "akb1_test.db"
    url = f"sqlite+aiosqlite:///{db_path}"
    os.environ["DATABASE_URL"] = url
    os.environ["SEED_DEMO_DATA"] = "false"
    get_settings.cache_clear()  # type: ignore[attr-defined]
    reset_engine_for_tests(url)
    yield url
    reset_engine_for_tests()


@pytest_asyncio.fixture()
async def session(tmp_db_url: str) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(tmp_db_url, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as s:
        yield s
    await engine.dispose()


@pytest_asyncio.fixture()
async def app_client(tmp_db_url: str) -> AsyncIterator[AsyncClient]:
    from app.main import create_app

    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        async with app.router.lifespan_context(app):
            yield client
