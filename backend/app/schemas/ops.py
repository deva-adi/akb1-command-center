from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ScenarioExecutionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_name: str
    execution_date: datetime | None = None
    triggered_by: str | None = None
    status: str | None = None
    details: str | None = None
    financial_impact: float | None = None
    outcome_notes: str | None = None


class ResourcePoolOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    role: str | None = None
    role_tier: str | None = None
    skill_set: str | None = None
    current_program_id: int | None = None
    current_project_id: int | None = None
    utilization_pct: float | None = None
    bench_days: int
    loaded_cost_annual: float | None = None
    status: str


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action: str | None = None
    table_name: str | None = None
    record_id: int | None = None
    old_value: str | None = None
    new_value: str | None = None
    user_action: str | None = None
    timestamp: datetime
