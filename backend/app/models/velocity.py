from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SprintVelocityDual(Base):
    __tablename__ = "sprint_velocity_dual"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    sprint_number: Mapped[int | None] = mapped_column(Integer)
    standard_velocity: Mapped[float | None] = mapped_column(Float)
    ai_raw_velocity: Mapped[float | None] = mapped_column(Float)
    ai_rework_points: Mapped[float | None] = mapped_column(Float)
    ai_quality_adjusted_velocity: Mapped[float | None] = mapped_column(Float)
    combined_velocity: Mapped[float | None] = mapped_column(Float)
    merge_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    quality_parity_ratio: Mapped[float | None] = mapped_column(Float)
    snapshot_date: Mapped[date | None] = mapped_column(Date)


class SprintVelocityBlendRule(Base):
    __tablename__ = "sprint_velocity_blend_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    gate_name: Mapped[str] = mapped_column(String, nullable=False)
    gate_condition: Mapped[str | None] = mapped_column(String)
    current_value: Mapped[float | None] = mapped_column(Float)
    threshold: Mapped[float | None] = mapped_column(Float)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    last_evaluated: Mapped[date | None] = mapped_column(Date)
