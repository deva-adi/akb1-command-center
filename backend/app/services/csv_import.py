"""CSV import commit + rollback.

Two entity types are supported today:
- `programmes` → rows go into `programs` (and existing codes are updated)
- `kpi_monthly` → rows go into `kpi_snapshots`, keyed by KPI code + programme.

Rollback works by taking a gzipped JSON snapshot of every row that
belonged to the affected tables *before* the import ran. When the user
clicks rollback we wipe those tables of rows matching the snapshot's
primary keys and re-insert the captured state.

Keep scope small — we deliberately don't support the full 15 CSV
templates yet. Extensions go in SCHEMA_REGISTRY.
"""
from __future__ import annotations

import csv
import gzip
import io
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    DataImport,
    DataImportSnapshot,
    KpiDefinition,
    KpiSnapshot,
    Program,
)


class CsvImportError(ValueError):
    """Raised when a CSV file can't be committed."""


@dataclass(frozen=True)
class CommitResult:
    import_id: int
    snapshot_id: int
    rows_imported: int
    affected_tables: list[str]


@dataclass(frozen=True)
class RollbackResult:
    import_id: int
    status: str
    rows_restored: int


def _parse_rows(raw_bytes: bytes) -> list[dict[str, str]]:
    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CsvImportError("CSV must be UTF-8 encoded") from exc
    reader = csv.DictReader(io.StringIO(text))
    return [
        {k.strip(): (v or "").strip() for k, v in row.items() if k is not None}
        for row in reader
    ]


def _parse_date(value: str, *, field: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise CsvImportError(f"Row has invalid date in column '{field}': {value}") from exc


def _parse_float(value: str, *, field: str, optional: bool = True) -> float | None:
    if value in ("", None):
        if optional:
            return None
        raise CsvImportError(f"Row missing required numeric column '{field}'")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise CsvImportError(f"Row has invalid number in column '{field}': {value}") from exc


def _parse_int(value: str, *, field: str, optional: bool = True) -> int | None:
    if value in ("", None):
        if optional:
            return None
        raise CsvImportError(f"Row missing required integer column '{field}'")
    try:
        return int(float(value))
    except (TypeError, ValueError) as exc:
        raise CsvImportError(f"Row has invalid integer in column '{field}': {value}") from exc


# ---------------------------------------------------------------------------
# Programme importer
# ---------------------------------------------------------------------------


async def _snapshot_programmes(
    session: AsyncSession, codes: list[str]
) -> list[dict[str, Any]]:
    if not codes:
        return []
    stmt = select(Program).where(Program.code.in_(codes))
    rows = (await session.execute(stmt)).scalars().all()
    return [_row_to_dict(r) for r in rows]


async def _commit_programmes(
    session: AsyncSession, rows: list[dict[str, str]]
) -> tuple[int, dict[str, Any], list[str]]:
    required = {"name", "code", "start_date"}
    if not rows:
        raise CsvImportError("CSV contains no rows")
    missing = required - set(rows[0].keys())
    if missing:
        raise CsvImportError(
            f"CSV missing required columns: {sorted(missing)}"
        )

    codes = [r["code"] for r in rows if r.get("code")]
    pre_rows = await _snapshot_programmes(session, codes)
    pre_codes = {r["code"] for r in pre_rows}
    snapshot = {"pre_rows": pre_rows, "scope_codes": codes, "pre_codes": sorted(pre_codes)}

    count = 0
    for raw in rows:
        if not raw.get("code") or not raw.get("name"):
            raise CsvImportError("Each row needs a non-empty 'code' and 'name'")
        start_date = _parse_date(raw["start_date"], field="start_date")
        end_date = (
            _parse_date(raw["end_date"], field="end_date") if raw.get("end_date") else None
        )
        payload = {
            "name": raw["name"],
            "code": raw["code"],
            "client": raw.get("client") or None,
            "start_date": start_date,
            "end_date": end_date,
            "status": raw.get("status") or "Active",
            "bac": _parse_float(raw.get("bac", ""), field="bac"),
            "revenue": _parse_float(raw.get("revenue", ""), field="revenue"),
            "team_size": _parse_int(raw.get("team_size", ""), field="team_size"),
            "offshore_ratio": _parse_float(
                raw.get("offshore_ratio", ""), field="offshore_ratio"
            ),
            "delivery_model": raw.get("delivery_model") or None,
            "currency_code": raw.get("currency_code") or "INR",
        }
        existing = (
            await session.execute(select(Program).where(Program.code == raw["code"]))
        ).scalar_one_or_none()
        if existing is None:
            session.add(Program(**payload))
        else:
            for k, v in payload.items():
                setattr(existing, k, v)
        count += 1
    return count, snapshot, ["programs"]


# ---------------------------------------------------------------------------
# KPI monthly importer
# ---------------------------------------------------------------------------


async def _snapshot_kpi_monthly(
    session: AsyncSession,
    program_ids: list[int],
    kpi_ids: list[int],
    dates: list[date],
) -> list[dict[str, Any]]:
    if not (program_ids and kpi_ids and dates):
        return []
    stmt = select(KpiSnapshot).where(
        KpiSnapshot.program_id.in_(program_ids),
        KpiSnapshot.kpi_id.in_(kpi_ids),
        KpiSnapshot.snapshot_date.in_(dates),
    )
    rows = (await session.execute(stmt)).scalars().all()
    return [_row_to_dict(r) for r in rows]


async def _commit_kpi_monthly(
    session: AsyncSession, rows: list[dict[str, str]]
) -> tuple[int, dict[str, Any], list[str]]:
    required = {"program_code", "kpi_code", "snapshot_date", "value"}
    if not rows:
        raise CsvImportError("CSV contains no rows")
    missing = required - set(rows[0].keys())
    if missing:
        raise CsvImportError(
            f"CSV missing required columns: {sorted(missing)}"
        )

    programmes = await session.execute(select(Program.code, Program.id))
    programme_ids_by_code = {code: pid for code, pid in programmes.all()}
    kpis = await session.execute(select(KpiDefinition.code, KpiDefinition.id))
    kpi_ids_by_code = {code: kid for code, kid in kpis.all()}

    affected_program_ids: set[int] = set()
    affected_kpi_ids: set[int] = set()
    affected_dates: set[date] = set()

    # First pass: validate + collect scope for snapshot.
    resolved: list[dict[str, Any]] = []
    for raw in rows:
        program_id = programme_ids_by_code.get(raw.get("program_code", ""))
        if program_id is None:
            raise CsvImportError(f"Unknown programme code: {raw.get('program_code')!r}")
        kpi_id = kpi_ids_by_code.get(raw.get("kpi_code", ""))
        if kpi_id is None:
            raise CsvImportError(f"Unknown KPI code: {raw.get('kpi_code')!r}")
        snapshot_date = _parse_date(raw["snapshot_date"], field="snapshot_date")
        value = _parse_float(raw.get("value", ""), field="value", optional=False)
        resolved.append(
            {
                "program_id": program_id,
                "kpi_id": kpi_id,
                "snapshot_date": snapshot_date,
                "value": value,
                "notes": raw.get("notes") or None,
            }
        )
        affected_program_ids.add(program_id)
        affected_kpi_ids.add(kpi_id)
        affected_dates.add(snapshot_date)

    pre_rows = await _snapshot_kpi_monthly(
        session,
        sorted(affected_program_ids),
        sorted(affected_kpi_ids),
        sorted(affected_dates),
    )
    snapshot = {
        "pre_rows": pre_rows,
        "scope": {
            "program_ids": sorted(affected_program_ids),
            "kpi_ids": sorted(affected_kpi_ids),
            "snapshot_dates": sorted(d.isoformat() for d in affected_dates),
        },
    }

    # Second pass: delete colliding rows, insert fresh.
    await session.execute(
        delete(KpiSnapshot).where(
            KpiSnapshot.program_id.in_(affected_program_ids),
            KpiSnapshot.kpi_id.in_(affected_kpi_ids),
            KpiSnapshot.snapshot_date.in_(affected_dates),
        )
    )
    count = 0
    for payload in resolved:
        session.add(KpiSnapshot(**payload))
        count += 1

    return count, snapshot, ["kpi_snapshots"]


# ---------------------------------------------------------------------------
# Public registry + commit / rollback entry points
# ---------------------------------------------------------------------------


Importer = Callable[
    [AsyncSession, list[dict[str, str]]],
    Awaitable[tuple[int, dict[str, Any], list[str]]],
]

SCHEMA_REGISTRY: dict[str, dict[str, Any]] = {
    "programmes": {
        "label": "Programmes",
        "importer": _commit_programmes,
        "expected_columns": [
            "name",
            "code",
            "client",
            "start_date",
            "end_date",
            "status",
            "bac",
            "revenue",
            "team_size",
            "offshore_ratio",
            "delivery_model",
        ],
    },
    "kpi_monthly": {
        "label": "KPI monthly snapshots",
        "importer": _commit_kpi_monthly,
        "expected_columns": ["program_code", "kpi_code", "snapshot_date", "value", "notes"],
    },
}


async def commit_csv(
    session: AsyncSession,
    *,
    filename: str,
    entity_type: str,
    raw_bytes: bytes,
) -> CommitResult:
    if entity_type not in SCHEMA_REGISTRY:
        raise CsvImportError(
            f"Unsupported entity_type '{entity_type}'. "
            f"Supported: {sorted(SCHEMA_REGISTRY)}"
        )

    rows = _parse_rows(raw_bytes)
    importer: Importer = SCHEMA_REGISTRY[entity_type]["importer"]
    rows_imported, snapshot_payload, affected_tables = await importer(session, rows)

    snapshot_blob = gzip.compress(
        json.dumps(snapshot_payload, default=str).encode("utf-8")
    )

    snapshot = DataImportSnapshot(
        source_filename=filename,
        source_format="csv",
        row_count=rows_imported,
        affected_tables=json.dumps(affected_tables),
        pre_import_state=snapshot_blob,
        status="committed",
    )
    session.add(snapshot)
    await session.flush()

    import_row = DataImport(
        source=entity_type,
        file_name=filename,
        rows_imported=rows_imported,
        status="committed",
        column_mapping=json.dumps(
            {"entity_type": entity_type, "snapshot_id": snapshot.id}
        ),
        notes=f"Imported {rows_imported} rows into {', '.join(affected_tables)}",
    )
    session.add(import_row)
    await session.flush()
    await session.commit()
    return CommitResult(
        import_id=import_row.id,
        snapshot_id=snapshot.id,
        rows_imported=rows_imported,
        affected_tables=affected_tables,
    )


async def rollback_import(
    session: AsyncSession,
    *,
    import_id: int,
) -> RollbackResult:
    import_row = await session.get(DataImport, import_id)
    if import_row is None:
        raise CsvImportError(f"Unknown import id {import_id}")
    if import_row.status == "rolled_back":
        raise CsvImportError("Import was already rolled back.")

    meta = json.loads(import_row.column_mapping or "{}")
    snapshot_id = meta.get("snapshot_id")
    entity_type = meta.get("entity_type")
    if snapshot_id is None or entity_type not in SCHEMA_REGISTRY:
        raise CsvImportError(
            "Import has no restorable snapshot. Manual cleanup required."
        )

    snapshot_row = await session.get(DataImportSnapshot, snapshot_id)
    if snapshot_row is None or snapshot_row.pre_import_state is None:
        raise CsvImportError("Snapshot is missing; cannot roll back.")

    payload_bytes = gzip.decompress(snapshot_row.pre_import_state)
    snapshot_payload = json.loads(payload_bytes.decode("utf-8"))

    rows_restored = await _apply_rollback(session, entity_type, snapshot_payload)

    snapshot_row.status = "rolled_back"
    snapshot_row.rollback_timestamp = datetime.now(UTC)
    import_row.status = "rolled_back"
    await session.commit()
    return RollbackResult(
        import_id=import_id, status="rolled_back", rows_restored=rows_restored
    )


async def _apply_rollback(
    session: AsyncSession,
    entity_type: str,
    snapshot_payload: dict[str, Any],
) -> int:
    # Older snapshots stored just a list; treat that as pre_rows for backwards
    # compat with imports committed before this refactor.
    if isinstance(snapshot_payload, list):
        snapshot_payload = {"pre_rows": snapshot_payload}
    if entity_type == "programmes":
        return await _restore_programmes(session, snapshot_payload)
    if entity_type == "kpi_monthly":
        return await _restore_kpi_monthly(session, snapshot_payload)
    raise CsvImportError(f"No rollback handler for entity_type '{entity_type}'")


async def _restore_programmes(
    session: AsyncSession, payload: dict[str, Any]
) -> int:
    """Restore programmes to their pre-import state.

    scope_codes = every code that appeared in the CSV
    pre_rows    = state of those codes that existed before the import
    pre_codes   = subset of scope that existed before

    Rollback plan:
    1. Delete programmes whose code is in scope but not in pre_codes
       (they were created by the import).
    2. Restore the pre-state of programmes whose code was in pre_codes.
    """
    pre_rows = payload.get("pre_rows", [])
    scope_codes = set(payload.get("scope_codes", []))
    pre_codes = set(payload.get("pre_codes") or [row["code"] for row in pre_rows])
    new_codes = scope_codes - pre_codes

    if new_codes:
        await session.execute(delete(Program).where(Program.code.in_(new_codes)))

    drop = {"id", "created_at", "updated_at"}
    restored = 0
    for row in pre_rows:
        code = row["code"]
        existing = (
            await session.execute(select(Program).where(Program.code == code))
        ).scalar_one_or_none()
        if existing is None:
            session.add(Program(**_prepare_for_insert(row, drop)))
        else:
            for k, v in _prepare_for_insert(row, drop).items():
                setattr(existing, k, v)
        restored += 1
    return restored


async def _restore_kpi_monthly(
    session: AsyncSession, payload: dict[str, Any]
) -> int:
    """Restore kpi_snapshots to their pre-import state.

    Scope captures every (program_id, kpi_id, snapshot_date) key the CSV
    touched. Rollback wipes the whole scope first, then re-inserts the
    pre-rows — so rows that were net-new to the import are removed.
    """
    pre_rows = payload.get("pre_rows", [])
    scope = payload.get("scope") or {}
    scope_program_ids: set[int] = set(scope.get("program_ids") or [])
    scope_kpi_ids: set[int] = set(scope.get("kpi_ids") or [])
    scope_dates: set[date] = {
        _coerce_date(v) for v in (scope.get("snapshot_dates") or [])
    }

    # Older snapshots had no scope — fall back to derive it from pre_rows.
    if not scope_program_ids:
        scope_program_ids = {
            row["program_id"] for row in pre_rows if row.get("program_id") is not None
        }
    if not scope_kpi_ids:
        scope_kpi_ids = {
            row["kpi_id"] for row in pre_rows if row.get("kpi_id") is not None
        }
    if not scope_dates:
        scope_dates = {
            _coerce_date(row["snapshot_date"])
            for row in pre_rows
            if row.get("snapshot_date")
        }

    if scope_program_ids and scope_kpi_ids and scope_dates:
        await session.execute(
            delete(KpiSnapshot).where(
                KpiSnapshot.program_id.in_(scope_program_ids),
                KpiSnapshot.kpi_id.in_(scope_kpi_ids),
                KpiSnapshot.snapshot_date.in_(scope_dates),
            )
        )

    restored = 0
    for row in pre_rows:
        insert_payload = _prepare_for_insert(row, {"id", "created_at"})
        if insert_payload.get("snapshot_date"):
            insert_payload["snapshot_date"] = _coerce_date(insert_payload["snapshot_date"])
        session.add(KpiSnapshot(**insert_payload))
        restored += 1
    return restored


def _coerce_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise CsvImportError(f"Unexpected date value: {value!r}")


def _prepare_for_insert(
    row: dict[str, Any], drop_keys: set[str]
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in row.items():
        if key in drop_keys:
            continue
        if key.endswith("_date") and isinstance(value, str) and value:
            try:
                out[key] = date.fromisoformat(value)
                continue
            except ValueError:
                pass
        out[key] = value
    return out


def _row_to_dict(row: object) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for col in row.__table__.columns:  # type: ignore[attr-defined]
        value = getattr(row, col.name)
        if hasattr(value, "isoformat"):
            result[col.name] = value.isoformat()
        else:
            result[col.name] = value
    return result
