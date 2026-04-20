from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class KpiDefinitionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    formula: str
    description: str | None = None
    unit: str | None = None
    green_threshold: float | None = None
    amber_threshold: float | None = None
    red_threshold: float | None = None
    weight: float
    category: str | None = None
    is_higher_better: bool


class KpiSnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    kpi_id: int | None = None
    snapshot_date: date
    value: float
    trend: str | None = None
    notes: str | None = None
