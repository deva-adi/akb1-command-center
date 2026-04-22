"""One-time Alembic bootstrap for the AKB1 Command Center database.

Three volume states are possible when the backend starts:

  1. Fresh volume. No DB at all, or the DB file exists but has no tables.
     ``create_all`` primes the schema, then we stamp the ``alembic_version``
     row to ``head`` so future startups take the already-migrated path.

  2. Legacy v5.6 volume. Tables exist (the programs table in particular) but
     ``alembic_version`` is missing. This is what every deploy from v5.0
     through v5.6 left behind because main.py used ``Base.metadata.create_all``
     directly and never ran Alembic. We stamp to ``0002_add_backlog_items``
     (the latest revision before the v5.7.0 work), then run ``upgrade head``
     so only revision ``0003`` actually applies. Revisions ``0001`` and
     ``0002`` never execute in this path.

  3. Already migrated. ``alembic_version`` is present. We simply run
     ``upgrade head``, which is a no-op when the DB is at head and otherwise
     applies the outstanding revisions.

``ensure_migrations_applied`` is the single entry point. It is safe to call
repeatedly and is designed to be invoked from the FastAPI ``lifespan`` hook
before the rest of startup runs.

All logging goes through ``structlog`` via ``app.logging_config.get_logger``
so the three paths can be distinguished by a single grep on the container
output. Log event names are stable strings, see
``ensure_migrations_applied`` below for the exact values.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Literal

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.logging_config import get_logger
from app.models import Base

log = get_logger(__name__)

VolumeState = Literal["fresh", "legacy_v5_6", "already_migrated"]

_ALEMBIC_INI = Path(__file__).resolve().parents[2] / "alembic.ini"
# Revision id of the last migration that landed before v5.7.0.
_PRE_V5_7_REVISION = "0002_add_backlog_items"
# Head revision as of v5.7.0. Keep in sync with backend/alembic/versions/.
_HEAD_REVISION = "0003_add_pnl_columns_and_programme_rates"


def _detect_state(sync_url: str) -> VolumeState:
    """Classify the DB at ``sync_url`` into one of the three volume states."""
    eng = create_engine(sync_url)
    try:
        insp = inspect(eng)
        has_alembic = insp.has_table("alembic_version")
        has_programs = insp.has_table("programs")
    finally:
        eng.dispose()
    if has_alembic:
        return "already_migrated"
    if has_programs:
        return "legacy_v5_6"
    return "fresh"


def _detect_schema_revision(sync_url: str) -> str:
    """Infer which migration the live schema corresponds to.

    Used in the legacy path to decide whether the DB needs migration 0003
    applied or whether ``Base.metadata.create_all`` already primed the
    schema to v5.7.0 shape (as happens in test fixtures and any ad-hoc
    deploy that invoked create_all before stamping).
    """
    eng = create_engine(sync_url)
    try:
        insp = inspect(eng)
        has_programme_rates = insp.has_table("programme_rates")
        cs_cols = {c["name"] for c in insp.get_columns("commercial_scenarios")} if insp.has_table("commercial_scenarios") else set()
        has_billed_revenue = "billed_revenue" in cs_cols
        has_backlog_items = insp.has_table("backlog_items")
    finally:
        eng.dispose()
    if has_programme_rates and has_billed_revenue:
        return _HEAD_REVISION
    if has_backlog_items:
        return _PRE_V5_7_REVISION
    return "0001_initial_schema"


def _build_alembic_config(sync_url: str) -> Config:
    cfg = Config(str(_ALEMBIC_INI))
    cfg.set_main_option("sqlalchemy.url", sync_url)
    # Keep Alembic quiet during startup; the three log lines below are enough.
    cfg.attributes["configure_logger"] = False
    return cfg


@contextmanager
def _pin_env_url(sync_url: str) -> Iterator[None]:
    """Temporarily align DATABASE_SYNC_URL with the bootstrap target.

    The Alembic env.py at backend/alembic/env.py reads DATABASE_SYNC_URL and
    DATABASE_URL and overrides whatever sqlalchemy.url we set on the Config
    object. Without this guard, a stale env var from an earlier test or an
    unrelated process causes the bootstrap to target the wrong database.
    """
    prev_sync = os.environ.get("DATABASE_SYNC_URL")
    prev_async = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_SYNC_URL"] = sync_url
    # env.py falls back to DATABASE_URL when DATABASE_SYNC_URL is absent.
    # Clear it so the sync URL wins even if a caller set an inconsistent pair.
    os.environ.pop("DATABASE_URL", None)
    try:
        yield
    finally:
        if prev_sync is None:
            os.environ.pop("DATABASE_SYNC_URL", None)
        else:
            os.environ["DATABASE_SYNC_URL"] = prev_sync
        if prev_async is not None:
            os.environ["DATABASE_URL"] = prev_async


def ensure_migrations_applied(sync_url: str) -> VolumeState:
    """Bring the database at ``sync_url`` to head.

    Returns the volume state that was detected, so callers can assert on it
    from tests. Always leaves the DB at head on success.
    """
    state = _detect_state(sync_url)
    cfg = _build_alembic_config(sync_url)

    with _pin_env_url(sync_url):
        if state == "fresh":
            log.info(
                "migration_bootstrap.fresh_volume",
                message="migration_bootstrap: fresh volume detected, create_all will prime schema, then stamp to head",
            )
            eng = create_engine(sync_url)
            try:
                Base.metadata.create_all(eng)
            finally:
                eng.dispose()
            command.stamp(cfg, "head")
            return state

        if state == "legacy_v5_6":
            # Inspect the live schema to decide the starting revision. A
            # typical v5.6 volume is at 0002; a volume that was primed with
            # Base.metadata.create_all against v5.7.0 models (tests, or an
            # ad-hoc deploy) is already at head shape, no migrations to run.
            detected_rev = _detect_schema_revision(sync_url)
            if detected_rev == _HEAD_REVISION:
                log.info(
                    "migration_bootstrap.legacy_v5_6",
                    message=(
                        "migration_bootstrap: legacy volume detected "
                        "(alembic_version missing, programs table present), "
                        "schema already at head shape, stamping directly to head"
                    ),
                    detected_revision=detected_rev,
                )
                command.stamp(cfg, "head")
            else:
                log.info(
                    "migration_bootstrap.legacy_v5_6",
                    message=(
                        "migration_bootstrap: legacy volume detected "
                        "(alembic_version missing, programs table present), "
                        "stamping to 0002 then upgrading to head"
                    ),
                    detected_revision=detected_rev,
                )
                command.stamp(cfg, _PRE_V5_7_REVISION)
                command.upgrade(cfg, "head")
            return state

        # already_migrated
        log.info(
            "migration_bootstrap.already_migrated",
            message="migration_bootstrap: alembic_version present, running upgrade head (no-op if at head)",
        )
        command.upgrade(cfg, "head")
        return state
