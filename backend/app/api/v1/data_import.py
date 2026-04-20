from __future__ import annotations

import csv
import io
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import DataImport
from app.schemas.settings import DataImportLogOut

router = APIRouter(prefix="/import", tags=["import"])

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MiB


@router.get("/log", response_model=list[DataImportLogOut])
async def list_import_log(session: AsyncSession = Depends(get_session)) -> list[DataImport]:
    result = await session.execute(
        select(DataImport).order_by(DataImport.import_date.desc())
    )
    return list(result.scalars().all())


@router.post("/csv/preview", status_code=status.HTTP_200_OK)
async def preview_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Parse a CSV upload and return the detected columns plus a sample.

    Persistence lands with the rollback-capable importer (Iteration 2). This
    endpoint exists so Tab 11 can validate a file before commit.
    """
    del session  # Preview does not touch DB yet; wiring awaits Iteration 2.
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
        text = raw.decode("utf-8")
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
