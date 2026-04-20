from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class SprintVelocityDualOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    sprint_number: int | None = None
    standard_velocity: float | None = None
    ai_raw_velocity: float | None = None
    ai_rework_points: float | None = None
    ai_quality_adjusted_velocity: float | None = None
    combined_velocity: float | None = None
    merge_eligible: bool
    quality_parity_ratio: float | None = None
    snapshot_date: date | None = None


class BlendRuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    gate_name: str
    gate_condition: str | None = None
    current_value: float | None = None
    threshold: float | None = None
    passed: bool
    last_evaluated: date | None = None


class CommercialScenarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    scenario_name: str | None = None
    planned_revenue: float | None = None
    actual_revenue: float | None = None
    planned_cost: float | None = None
    actual_cost: float | None = None
    gross_margin_pct: float | None = None
    contribution_margin_pct: float | None = None
    portfolio_margin_pct: float | None = None
    net_margin_pct: float | None = None
    snapshot_date: date | None = None
    notes: str | None = None


class LossExposureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    snapshot_date: date | None = None
    loss_category: str
    amount: float | None = None
    percentage_of_revenue: float | None = None
    detection_method: str | None = None
    mitigation_status: str | None = None
    notes: str | None = None


class RateCardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    role_tier: str
    planned_rate: float
    actual_rate: float | None = None
    planned_headcount: int | None = None
    actual_headcount: int | None = None
    snapshot_date: date | None = None
    notes: str | None = None


class ChangeRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    cr_date: date | None = None
    cr_description: str | None = None
    effort_hours: float | None = None
    cr_value: float | None = None
    processing_cost: float | None = None
    status: str | None = None
    margin_impact: float | None = None
    is_billable: bool | None = None
