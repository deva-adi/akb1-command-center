from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class FlowMetrics(Base):
    __tablename__ = "flow_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    period_start: Mapped[date | None] = mapped_column(Date)
    period_end: Mapped[date | None] = mapped_column(Date)
    throughput_items: Mapped[int | None] = mapped_column(Integer)
    wip_avg: Mapped[float | None] = mapped_column(Numeric(6, 2))
    wip_limit: Mapped[int | None] = mapped_column(Integer)
    cycle_time_p50: Mapped[float | None] = mapped_column(Numeric(6, 2))
    cycle_time_p85: Mapped[float | None] = mapped_column(Numeric(6, 2))
    cycle_time_p95: Mapped[float | None] = mapped_column(Numeric(6, 2))
    lead_time_avg: Mapped[float | None] = mapped_column(Numeric(6, 2))
    blocked_time_hours: Mapped[float | None] = mapped_column(Numeric(6, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class ProjectPhase(Base):
    __tablename__ = "project_phases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    phase_name: Mapped[str] = mapped_column(String, nullable=False)
    phase_sequence: Mapped[int | None] = mapped_column(Integer)
    planned_start: Mapped[date | None] = mapped_column(Date)
    planned_end: Mapped[date | None] = mapped_column(Date)
    actual_start: Mapped[date | None] = mapped_column(Date)
    actual_end: Mapped[date | None] = mapped_column(Date)
    percent_complete: Mapped[float | None] = mapped_column(Numeric(5, 2))
    gate_status: Mapped[str | None] = mapped_column(String)
    gate_approver: Mapped[str | None] = mapped_column(String)
    gate_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)
