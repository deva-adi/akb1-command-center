from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AppSettingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str | None = None


class AppSettingUpdate(BaseModel):
    value: str | None = None


class DataImportLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_name: str | None = None
    source: str | None = None
    rows_imported: int | None = None
    status: str | None = None
    notes: str | None = None
