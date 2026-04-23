"""Tests for the Alembic bootstrap in app.db.migration_bootstrap.

Three volume states must be handled cleanly:

  A. Fresh volume. No DB file. create_all primes the schema, then the
     bootstrap stamps to head. ``alembic_version`` is present at the
     correct revision and the new v5.7.0 schema additions exist.

  B. Legacy v5.6 volume. Tables exist but ``alembic_version`` does not.
     This simulates every deploy from v5.0 through v5.6 on a volume that
     was built via ``Base.metadata.create_all`` only. The bootstrap must
     stamp to 0002 and upgrade to head, which applies only 0003. It must
     not attempt to reapply 0001 or 0002 against existing tables.

  C. Already migrated volume. Bootstrap is a no-op. No error, DB stays
     at head.
"""
from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, inspect, text

from app.db.migration_bootstrap import ensure_migrations_applied
from app.models import Base

_EXPECTED_HEAD = "0003_add_pnl_columns_and_programme_rates"
_PNL_COLUMNS = {
    "billed_revenue",
    "collected_revenue",
    "unbilled_wip",
    "ar_balance",
    "billing_ratio",
}


def _sync_url(db_path: Path) -> str:
    return f"sqlite:///{db_path}"


def _read_head(sync_url: str) -> str | None:
    eng = create_engine(sync_url)
    try:
        with eng.connect() as conn:
            row = conn.execute(text("SELECT version_num FROM alembic_version")).first()
            return row[0] if row else None
    finally:
        eng.dispose()


def _columns(sync_url: str, table: str) -> set[str]:
    eng = create_engine(sync_url)
    try:
        return {c["name"] for c in inspect(eng).get_columns(table)}
    finally:
        eng.dispose()


def _has_table(sync_url: str, table: str) -> bool:
    eng = create_engine(sync_url)
    try:
        return inspect(eng).has_table(table)
    finally:
        eng.dispose()


def test_bootstrap_fresh_volume_creates_schema_and_stamps_head(tmp_path: Path) -> None:
    """Test A: empty SQLite file, confirm create_all + stamp path ends at head."""
    db = tmp_path / "fresh.db"
    url = _sync_url(db)

    state = ensure_migrations_applied(url)

    assert state == "fresh"
    # Schema primed by create_all, then alembic_version stamped.
    assert _has_table(url, "alembic_version")
    assert _read_head(url) == _EXPECTED_HEAD
    # v5.7.0 schema additions are present because create_all reflects current models.
    assert _has_table(url, "programme_rates")
    assert _PNL_COLUMNS.issubset(_columns(url, "commercial_scenarios"))


def test_bootstrap_legacy_v5_6_volume_stamps_to_0002_then_upgrades(tmp_path: Path) -> None:
    """Test B: pre-populated v5.6 schema, no alembic_version row.

    Confirms the bootstrap stamps to 0002 and applies only 0003, without
    attempting to reapply 0001 or 0002 against existing tables. Uses
    ``create_all`` with current models then drops the v5.7.0-specific
    additions to recreate the v5.6 shape.
    """
    db = tmp_path / "legacy.db"
    url = _sync_url(db)
    eng = create_engine(url)
    try:
        Base.metadata.create_all(eng)
        with eng.begin() as conn:
            # Rewind to v5.6 shape: drop the new table and the five new columns.
            conn.execute(text("DROP TABLE programme_rates"))
            for col in (
                "billing_ratio",
                "ar_balance",
                "unbilled_wip",
                "collected_revenue",
                "billed_revenue",
            ):
                conn.execute(text(f"ALTER TABLE commercial_scenarios DROP COLUMN {col}"))
    finally:
        eng.dispose()

    # Pre-conditions match a v5.6 volume.
    assert _has_table(url, "programs")
    assert not _has_table(url, "alembic_version")
    assert not _has_table(url, "programme_rates")
    assert not _PNL_COLUMNS.intersection(_columns(url, "commercial_scenarios"))

    state = ensure_migrations_applied(url)

    assert state == "legacy_v5_6"
    assert _read_head(url) == _EXPECTED_HEAD
    # Migration 0003 ran: new table created and five columns added.
    assert _has_table(url, "programme_rates")
    assert _PNL_COLUMNS.issubset(_columns(url, "commercial_scenarios"))


def test_bootstrap_already_migrated_volume_is_noop(tmp_path: Path) -> None:
    """Test C: DB already at head, confirm bootstrap is a no-op."""
    db = tmp_path / "migrated.db"
    url = _sync_url(db)

    # First run brings the DB to head.
    first = ensure_migrations_applied(url)
    assert first == "fresh"
    assert _read_head(url) == _EXPECTED_HEAD

    # Second run must see already_migrated state and leave the DB at head.
    second = ensure_migrations_applied(url)
    assert second == "already_migrated"
    assert _read_head(url) == _EXPECTED_HEAD
    assert _has_table(url, "programme_rates")
    assert _PNL_COLUMNS.issubset(_columns(url, "commercial_scenarios"))
