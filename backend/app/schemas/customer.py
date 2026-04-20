from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class CustomerExpectationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    snapshot_date: date
    dimension: str
    expected_score: float | None = None
    delivered_score: float | None = None
    gap: float | None = None
    weight: float
    evidence_source: str | None = None
    owner: str | None = None
    notes: str | None = None


class CustomerActionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    meeting_date: date | None = None
    description: str
    owner: str | None = None
    due_date: date | None = None
    status: str
    priority: str | None = None
    escalated: bool
    resolution_notes: str | None = None
    closed_date: date | None = None
