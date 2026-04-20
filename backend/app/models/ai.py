from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AiTool(Base):
    __tablename__ = "ai_tools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    vendor: Mapped[str | None] = mapped_column(String)
    version: Mapped[str | None] = mapped_column(String)
    category: Mapped[str | None] = mapped_column(String)
    license_type: Mapped[str | None] = mapped_column(String)
    cost_per_seat: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="Active")


class AiToolAssignment(Base):
    __tablename__ = "ai_tool_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ai_tool_id: Mapped[int | None] = mapped_column(ForeignKey("ai_tools.id"))
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    assigned_date: Mapped[date | None] = mapped_column(Date)
    users_count: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="Active")


class AiUsageMetrics(Base):
    __tablename__ = "ai_usage_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ai_tool_id: Mapped[int | None] = mapped_column(ForeignKey("ai_tools.id"))
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    snapshot_date: Mapped[date | None] = mapped_column(Date)
    prompts_count: Mapped[int | None] = mapped_column(Integer)
    suggestions_accepted: Mapped[int | None] = mapped_column(Integer)
    suggestions_rejected: Mapped[int | None] = mapped_column(Integer)
    time_saved_hours: Mapped[float | None] = mapped_column(Float)
    cost: Mapped[float | None] = mapped_column(Float)


class AiCodeMetrics(Base):
    __tablename__ = "ai_code_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    sprint_number: Mapped[int | None] = mapped_column(Integer)
    ai_lines_generated: Mapped[int | None] = mapped_column(Integer)
    ai_lines_accepted: Mapped[int | None] = mapped_column(Integer)
    ai_defect_count: Mapped[int | None] = mapped_column(Integer)
    ai_test_coverage_pct: Mapped[float | None] = mapped_column(Float)
    ai_review_rejection_pct: Mapped[float | None] = mapped_column(Float)
    human_defect_count: Mapped[int | None] = mapped_column(Integer)
    human_test_coverage_pct: Mapped[float | None] = mapped_column(Float)
    human_review_rejection_pct: Mapped[float | None] = mapped_column(Float)
    snapshot_date: Mapped[date | None] = mapped_column(Date)


class AiSdlcMetrics(Base):
    __tablename__ = "ai_sdlc_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    sprint_number: Mapped[int | None] = mapped_column(Integer)
    estimation_accuracy_with_ai: Mapped[float | None] = mapped_column(Float)
    estimation_accuracy_without_ai: Mapped[float | None] = mapped_column(Float)
    code_review_hours_with_ai: Mapped[float | None] = mapped_column(Float)
    code_review_hours_without_ai: Mapped[float | None] = mapped_column(Float)
    planning_velocity_with_ai: Mapped[float | None] = mapped_column(Float)
    planning_velocity_without_ai: Mapped[float | None] = mapped_column(Float)
    documentation_hours_with_ai: Mapped[float | None] = mapped_column(Float)
    documentation_hours_without_ai: Mapped[float | None] = mapped_column(Float)
    snapshot_date: Mapped[date | None] = mapped_column(Date)


class AiTrustScore(Base):
    __tablename__ = "ai_trust_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ai_tool_id: Mapped[int | None] = mapped_column(ForeignKey("ai_tools.id"))
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    snapshot_date: Mapped[date | None] = mapped_column(Date)
    provenance_score: Mapped[float | None] = mapped_column(Float)
    review_status_score: Mapped[float | None] = mapped_column(Float)
    test_coverage_score: Mapped[float | None] = mapped_column(Float)
    drift_check_score: Mapped[float | None] = mapped_column(Float)
    override_rate_score: Mapped[float | None] = mapped_column(Float)
    defect_rate_score: Mapped[float | None] = mapped_column(Float)
    composite_score: Mapped[float | None] = mapped_column(Float)
    maturity_level: Mapped[str | None] = mapped_column(String)


class AiGovernanceConfig(Base):
    __tablename__ = "ai_governance_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    config_type: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    scope: Mapped[str | None] = mapped_column(String)
    enforcement_method: Mapped[str | None] = mapped_column(String)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    status: Mapped[str] = mapped_column(String, default="Active")
    compliance_pct: Mapped[float | None] = mapped_column(Float)
    last_audit_date: Mapped[date | None] = mapped_column(Date)
    review_date: Mapped[date | None] = mapped_column(Date)
    owner: Mapped[str | None] = mapped_column(String)


class AiOverrideLog(Base):
    __tablename__ = "ai_override_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ai_tool_id: Mapped[int | None] = mapped_column(ForeignKey("ai_tools.id"))
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    override_date: Mapped[datetime | None] = mapped_column(DateTime)
    override_type: Mapped[str | None] = mapped_column(String)
    reason: Mapped[str | None] = mapped_column(Text)
    outcome: Mapped[str | None] = mapped_column(Text)
    approver: Mapped[str | None] = mapped_column(String)
