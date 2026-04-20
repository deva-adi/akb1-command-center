from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class SprintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    sprint_number: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    planned_points: int | None = None
    completed_points: int | None = None
    velocity: float | None = None
    defects_found: int | None = None
    defects_fixed: int | None = None
    rework_hours: float | None = None
    team_size: int | None = None
    ai_assisted_points: int
    iteration_type: str
    estimation_unit: str


class EvmSnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    snapshot_date: date
    planned_value: float
    earned_value: float
    actual_cost: float
    percent_complete: float | None = None
    bac: float | None = None
    cpi: float | None = None
    spi: float | None = None
    eac: float | None = None
    tcpi: float | None = None
    vac: float | None = None
    notes: str | None = None


class FlowMetricsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int | None = None
    period_start: date | None = None
    period_end: date | None = None
    throughput_items: int | None = None
    wip_avg: float | None = None
    wip_limit: int | None = None
    cycle_time_p50: float | None = None
    cycle_time_p85: float | None = None
    cycle_time_p95: float | None = None
    lead_time_avg: float | None = None
    blocked_time_hours: float | None = None
    created_at: datetime


class ProjectPhaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int | None = None
    phase_name: str
    phase_sequence: int | None = None
    planned_start: date | None = None
    planned_end: date | None = None
    actual_start: date | None = None
    actual_end: date | None = None
    percent_complete: float | None = None
    gate_status: str | None = None
    gate_approver: str | None = None
    gate_date: date | None = None
    notes: str | None = None


class MilestoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    name: str
    planned_date: date
    actual_date: date | None = None
    status: str
    dependencies: str | None = None
    owner: str | None = None
    notes: str | None = None
