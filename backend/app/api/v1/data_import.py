from __future__ import annotations

import csv
import io
from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.models import DataImport
from app.rate_limit import limiter
from app.schemas.settings import DataImportLogOut
from app.services.csv_import import (
    SCHEMA_REGISTRY,
    CsvImportError,
    commit_csv,
    rollback_import,
)

router = APIRouter(prefix="/import", tags=["import"])

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MiB
_upload_limit = get_settings().rate_limit_upload
_write_limit = get_settings().rate_limit_write


@router.get("/log", response_model=list[DataImportLogOut])
async def list_import_log(session: AsyncSession = Depends(get_session)) -> list[DataImport]:
    result = await session.execute(
        select(DataImport).order_by(DataImport.import_date.desc())
    )
    return list(result.scalars().all())


@router.get("/schemas")
async def list_supported_schemas() -> dict[str, dict[str, Any]]:
    """Return the entity types the commit endpoint can accept today."""
    return {
        name: {
            "label": cfg["label"],
            "expected_columns": cfg["expected_columns"],
        }
        for name, cfg in SCHEMA_REGISTRY.items()
    }


@router.post("/csv/preview", status_code=status.HTTP_200_OK)
@limiter.limit(_upload_limit)
async def preview_csv(
    request: Request,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Parse a CSV upload and return the detected columns plus a sample."""
    del session  # Preview does not persist.
    allowed = {"text/csv", "application/vnd.ms-excel", "application/octet-stream"}
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported content type: {file.content_type}",
        )
    raw = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="CSV exceeds 10 MiB preview limit",
        )
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV must be UTF-8 encoded",
        ) from exc
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Empty CSV"
        )
    header, *data_rows = rows
    sample = [dict(zip(header, row, strict=False)) for row in data_rows[:5]]
    return {
        "filename": file.filename,
        "columns": header,
        "row_count": len(data_rows),
        "sample": sample,
    }


@router.post("/csv/commit", status_code=status.HTTP_201_CREATED)
@limiter.limit(_upload_limit)
async def commit_csv_endpoint(
    request: Request,
    entity_type: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Persist an uploaded CSV into the matching entity tables.

    Captures a pre-import snapshot into data_import_snapshots so the
    operation can be rolled back later via POST /import/{id}/rollback.
    """
    raw = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="CSV exceeds 10 MiB commit limit",
        )
    try:
        result = await commit_csv(
            session,
            filename=file.filename or "upload.csv",
            entity_type=entity_type,
            raw_bytes=raw,
        )
    except CsvImportError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

    return {
        "import_id": result.import_id,
        "snapshot_id": result.snapshot_id,
        "rows_imported": result.rows_imported,
        "affected_tables": result.affected_tables,
        "status": "committed",
    }


@router.post("/{import_id}/rollback", status_code=status.HTTP_200_OK)
@limiter.limit(_write_limit)
async def rollback_import_endpoint(
    request: Request,
    import_id: int,
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Restore the pre-import snapshot for the given import_id."""
    try:
        result = await rollback_import(session, import_id=import_id)
    except CsvImportError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    return {
        "import_id": result.import_id,
        "status": result.status,
        "rows_restored": result.rows_restored,
    }
