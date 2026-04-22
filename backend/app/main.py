from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.router import api_router
from app.config import Settings, get_settings
from app.database import dispose_engine, get_engine, get_session_factory
from app.db.migration_bootstrap import ensure_migrations_applied
from app.logging_config import configure_logging, get_logger
from app.models import Base
from app.rate_limit import limiter
from app.seed import seed_demo_data

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = get_settings()
    configure_logging(settings.log_level)
    log.info(
        "startup",
        app=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )

    # Bring the DB to head via Alembic. Three volume states handled:
    # fresh, legacy v5.6, or already migrated. See migration_bootstrap.
    # Runs on a worker thread because Alembic is synchronous.
    await asyncio.to_thread(ensure_migrations_applied, settings.database_sync_url)

    # Safety net: create_all is a no-op once the bootstrap above has run,
    # but it rescues the case where someone drops a table by hand.
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if settings.seed_demo_data:
        factory = get_session_factory()
        async with factory() as session:
            inserted = await seed_demo_data(session)
            log.info("seed.complete", inserted=inserted)

    try:
        yield
    finally:
        await dispose_engine()
        log.info("shutdown")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    # Legacy top-level health route — useful for simple liveness probes.
    from app.api.v1.health import router as health_router

    app.include_router(health_router)

    return app


app = create_app()
