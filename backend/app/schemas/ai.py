from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AiToolOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    vendor: str | None = None
    version: str | None = None
    category: str | None = None
    license_type: str | None = None
    cost_per_seat: float | None = None
    status: str


class AiToolAssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ai_tool_id: int | None = None
    program_id: int | None = None
    project_id: int | None = None
    assigned_date: date | None = None
    users_count: int | None = None
    status: str


class AiUsageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ai_tool_id: int | None = None
    program_id: int | None = None
    snapshot_date: date | None = None
    prompts_count: int | None = None
    suggestions_accepted: int | None = None
    suggestions_rejected: int | None = None
    time_saved_hours: float | None = None
    cost: float | None = None


class AiCodeMetricsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    sprint_number: int | None = None
    ai_lines_generated: int | None = None
    ai_lines_accepted: int | None = None
    ai_defect_count: int | None = None
    ai_test_coverage_pct: float | None = None
    ai_review_rejection_pct: float | None = None
    human_defect_count: int | None = None
    human_test_coverage_pct: float | None = None
    human_review_rejection_pct: float | None = None
    snapshot_date: date | None = None


class AiSdlcMetricsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    sprint_number: int | None = None
    estimation_accuracy_with_ai: float | None = None
    estimation_accuracy_without_ai: float | None = None
    code_review_hours_with_ai: float | None = None
    code_review_hours_without_ai: float | None = None
    planning_velocity_with_ai: float | None = None
    planning_velocity_without_ai: float | None = None
    documentation_hours_with_ai: float | None = None
    documentation_hours_without_ai: float | None = None
    snapshot_date: date | None = None


class AiTrustScoreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ai_tool_id: int | None = None
    program_id: int | None = None
    snapshot_date: date | None = None
    provenance_score: float | None = None
    review_status_score: float | None = None
    test_coverage_score: float | None = None
    drift_check_score: float | None = None
    override_rate_score: float | None = None
    defect_rate_score: float | None = None
    composite_score: float | None = None
    maturity_level: str | None = None


class AiGovernanceConfigOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    config_type: str
    name: str
    description: str | None = None
    scope: str | None = None
    enforcement_method: str | None = None
    program_id: int | None = None
    status: str
    compliance_pct: float | None = None
    last_audit_date: date | None = None
    review_date: date | None = None
    owner: str | None = None


class AiOverrideOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ai_tool_id: int | None = None
    program_id: int | None = None
    project_id: int | None = None
    override_date: datetime | None = None
    override_type: str | None = None
    reason: str | None = None
    outcome: str | None = None
    approver: str | None = None
