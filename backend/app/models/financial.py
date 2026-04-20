from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class BenchTracking(Base):
    __tablename__ = "bench_tracking"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    snapshot_date: Mapped[date | None] = mapped_column(Date)
    planned_headcount: Mapped[int | None] = mapped_column(Integer)
    actual_headcount: Mapped[int | None] = mapped_column(Integer)
    bench_headcount: Mapped[int | None] = mapped_column(Integer)
    loaded_cost_per_head: Mapped[float | None] = mapped_column(Float)
    shadow_allocation_cost: Mapped[float | None] = mapped_column(Float)
    allocation_method: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)


class ScopeCreepLog(Base):
    __tablename__ = "scope_creep_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    cr_date: Mapped[date | None] = mapped_column(Date)
    cr_description: Mapped[str | None] = mapped_column(Text)
    effort_hours: Mapped[float | None] = mapped_column(Float)
    cr_value: Mapped[float | None] = mapped_column(Float)
    processing_cost: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str | None] = mapped_column(String)
    margin_impact: Mapped[float | None] = mapped_column(Float)
    is_billable: Mapped[bool | None] = mapped_column(Boolean)


class LossExposure(Base):
    __tablename__ = "loss_exposure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    snapshot_date: Mapped[date | None] = mapped_column(Date)
    loss_category: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float | None] = mapped_column(Float)
    percentage_of_revenue: Mapped[float | None] = mapped_column(Float)
    detection_method: Mapped[str | None] = mapped_column(String)
    mitigation_status: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
