from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ProgrammeBase(BaseModel):
    name: str
    code: str
    client: str | None = None
    start_date: date
    end_date: date | None = None
    status: str = "Active"
    bac: float | None = None
    revenue: float | None = None
    team_size: int | None = None
    offshore_ratio: float | None = None
    delivery_model: str | None = None
    currency_code: str = "INR"


class ProgrammeCreate(ProgrammeBase):
    pass


class ProgrammeOut(ProgrammeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProjectBase(BaseModel):
    program_id: int | None = None
    name: str
    code: str
    start_date: date | None = None
    end_date: date | None = None
    status: str = "Active"
    bac: float | None = None
    revenue: float | None = None
    team_size: int | None = None
    tech_stack: str | None = None
    is_ai_augmented: bool = False
    ai_augmentation_level: str | None = None
    delivery_methodology: str = "Scrum"


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProgrammeWithProjects(ProgrammeOut):
    projects: list[ProjectOut] = Field(default_factory=list)
