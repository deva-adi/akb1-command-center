from __future__ import annotations

from datetime import date, datetime

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


class CustomerSatisfactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    snapshot_date: date
    csat_score: float | None = None
    nps_score: float | None = None
    escalation_count: int
    escalation_open: int
    steering_meetings_planned: int | None = None
    steering_meetings_held: int | None = None
    action_items_open: int | None = None
    action_items_closed: int | None = None
    positive_themes: str | None = None
    concern_themes: str | None = None
    renewal_score: float | None = None
    notes: str | None = None


class SlaIncidentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    incident_id: str | None = None
    priority: str
    summary: str | None = None
    reported_at: datetime
    responded_at: datetime | None = None
    resolved_at: datetime | None = None
    response_time_minutes: float | None = None
    resolution_time_minutes: float | None = None
    sla_breached: bool
    penalty_amount: float
    root_cause: str | None = None
    notes: str | None = None
