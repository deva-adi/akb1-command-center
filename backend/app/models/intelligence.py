from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Milestone(Base):
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    planned_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String, default="Pending")
    dependencies: Mapped[str | None] = mapped_column(Text)
    owner: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)


class SlaIncident(Base):
    __tablename__ = "sla_incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    incident_id: Mapped[str | None] = mapped_column(String)
    priority: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    reported_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    responded_at: Mapped[datetime | None] = mapped_column(DateTime)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime)
    response_time_minutes: Mapped[float | None] = mapped_column(Float)
    resolution_time_minutes: Mapped[float | None] = mapped_column(Float)
    sla_breached: Mapped[bool] = mapped_column(Boolean, default=False)
    penalty_amount: Mapped[float] = mapped_column(Float, default=0.0)
    root_cause: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)


class RateCard(Base):
    __tablename__ = "rate_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    role_tier: Mapped[str] = mapped_column(String, nullable=False)
    planned_rate: Mapped[float] = mapped_column(Float, nullable=False)
    actual_rate: Mapped[float | None] = mapped_column(Float)
    planned_headcount: Mapped[int | None] = mapped_column(Integer)
    actual_headcount: Mapped[int | None] = mapped_column(Integer)
    snapshot_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)


class UtilizationDetail(Base):
    __tablename__ = "utilization_detail"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    hris_utilization: Mapped[float | None] = mapped_column(Float)
    rm_utilization: Mapped[float | None] = mapped_column(Float)
    billing_utilization: Mapped[float | None] = mapped_column(Float)
    gap_leave_holidays: Mapped[float | None] = mapped_column(Float)
    gap_bench_rotation: Mapped[float | None] = mapped_column(Float)
    gap_rework_quality: Mapped[float | None] = mapped_column(Float)
    gap_meetings_admin: Mapped[float | None] = mapped_column(Float)
    gap_transition_churn: Mapped[float | None] = mapped_column(Float)
    gap_other: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)


class CustomerSatisfaction(Base):
    __tablename__ = "customer_satisfaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    csat_score: Mapped[float | None] = mapped_column(Float)
    nps_score: Mapped[float | None] = mapped_column(Float)
    escalation_count: Mapped[int] = mapped_column(Integer, default=0)
    escalation_open: Mapped[int] = mapped_column(Integer, default=0)
    steering_meetings_planned: Mapped[int | None] = mapped_column(Integer)
    steering_meetings_held: Mapped[int | None] = mapped_column(Integer)
    action_items_open: Mapped[int | None] = mapped_column(Integer)
    action_items_closed: Mapped[int | None] = mapped_column(Integer)
    positive_themes: Mapped[str | None] = mapped_column(Text)
    concern_themes: Mapped[str | None] = mapped_column(Text)
    renewal_score: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)


class KpiForecast(Base):
    __tablename__ = "kpi_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    kpi_id: Mapped[int | None] = mapped_column(ForeignKey("kpi_definitions.id"))
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    forecast_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_pct: Mapped[float | None] = mapped_column(Float)
    model_type: Mapped[str | None] = mapped_column(String)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class NarrativeCache(Base):
    __tablename__ = "narrative_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[int | None] = mapped_column(Integer)
    narrative_text: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    valid_until: Mapped[datetime | None] = mapped_column(DateTime)
