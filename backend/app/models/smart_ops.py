from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ResourcePool(Base):
    __tablename__ = "resource_pool"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str | None] = mapped_column(String)
    role_tier: Mapped[str | None] = mapped_column(String)
    skill_set: Mapped[str | None] = mapped_column(String)
    current_program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    current_project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    utilization_pct: Mapped[float | None] = mapped_column(Float)
    bench_days: Mapped[int] = mapped_column(Integer, default=0)
    loaded_cost_annual: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="Active")


class ScenarioExecution(Base):
    __tablename__ = "scenario_executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_name: Mapped[str] = mapped_column(String, nullable=False)
    execution_date: Mapped[datetime | None] = mapped_column(DateTime)
    triggered_by: Mapped[str | None] = mapped_column(String)
    status: Mapped[str | None] = mapped_column(String)
    details: Mapped[str | None] = mapped_column(Text)
    financial_impact: Mapped[float | None] = mapped_column(Float)
    outcome_notes: Mapped[str | None] = mapped_column(Text)
