from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RiskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int | None = None
    project_id: int | None = None
    title: str
    description: str | None = None
    category: str | None = None
    probability: float | None = None
    impact: float | None = None
    severity: str | None = None
    status: str
    owner: str | None = None
    mitigation_plan: str | None = None
    escalated_to_programme: bool
