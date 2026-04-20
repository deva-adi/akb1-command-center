from __future__ import annotations

from datetime import date

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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    client: Mapped[str | None] = mapped_column(String)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String, default="Active")
    bac: Mapped[float | None] = mapped_column(Float)
    revenue: Mapped[float | None] = mapped_column(Float)
    team_size: Mapped[int | None] = mapped_column(Integer)
    offshore_ratio: Mapped[float | None] = mapped_column(Float)
    delivery_model: Mapped[str | None] = mapped_column(String)
    currency_code: Mapped[str] = mapped_column(String, default="INR")
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    projects: Mapped[list[Project]] = relationship(back_populates="program")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String, default="Active")
    bac: Mapped[float | None] = mapped_column(Float)
    revenue: Mapped[float | None] = mapped_column(Float)
    team_size: Mapped[int | None] = mapped_column(Integer)
    tech_stack: Mapped[str | None] = mapped_column(String)
    is_ai_augmented: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_augmentation_level: Mapped[str | None] = mapped_column(String)
    delivery_methodology: Mapped[str] = mapped_column(String, default="Scrum")
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.current_timestamp())

    program: Mapped[Program | None] = relationship(back_populates="projects")


class KpiDefinition(Base):
    __tablename__ = "kpi_definitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    formula: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String)
    green_threshold: Mapped[float | None] = mapped_column(Float)
    amber_threshold: Mapped[float | None] = mapped_column(Float)
    red_threshold: Mapped[float | None] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    category: Mapped[str | None] = mapped_column(String)
    is_higher_better: Mapped[bool] = mapped_column(Boolean, default=True)


class KpiSnapshot(Base):
    __tablename__ = "kpi_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    kpi_id: Mapped[int | None] = mapped_column(ForeignKey("kpi_definitions.id"))
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    trend: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.current_timestamp())


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String)
    probability: Mapped[float | None] = mapped_column(Float)
    impact: Mapped[float | None] = mapped_column(Float)
    severity: Mapped[str | None] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="Open")
    owner: Mapped[str | None] = mapped_column(String)
    mitigation_plan: Mapped[str | None] = mapped_column(Text)
    escalated_to_programme: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


class RiskHistory(Base):
    __tablename__ = "risk_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    risk_id: Mapped[int | None] = mapped_column(ForeignKey("risks.id"))
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    probability: Mapped[float | None] = mapped_column(Float)
    impact: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)


class Initiative(Base):
    __tablename__ = "initiatives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[str | None] = mapped_column(String)
    score: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="Proposed")
    owner: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.current_timestamp())


class SprintData(Base):
    __tablename__ = "sprint_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    sprint_number: Mapped[int | None] = mapped_column(Integer)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    planned_points: Mapped[int | None] = mapped_column(Integer)
    completed_points: Mapped[int | None] = mapped_column(Integer)
    velocity: Mapped[float | None] = mapped_column(Float)
    defects_found: Mapped[int | None] = mapped_column(Integer)
    defects_fixed: Mapped[int | None] = mapped_column(Integer)
    rework_hours: Mapped[float | None] = mapped_column(Float)
    team_size: Mapped[int | None] = mapped_column(Integer)
    ai_assisted_points: Mapped[int] = mapped_column(Integer, default=0)
    iteration_type: Mapped[str] = mapped_column(String, default="Sprint")
    estimation_unit: Mapped[str] = mapped_column(String, default="StoryPoints")
    notes: Mapped[str | None] = mapped_column(Text)


class CommercialScenario(Base):
    __tablename__ = "commercial_scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    scenario_name: Mapped[str | None] = mapped_column(String)
    planned_revenue: Mapped[float | None] = mapped_column(Float)
    actual_revenue: Mapped[float | None] = mapped_column(Float)
    planned_cost: Mapped[float | None] = mapped_column(Float)
    actual_cost: Mapped[float | None] = mapped_column(Float)
    gross_margin_pct: Mapped[float | None] = mapped_column(Float)
    contribution_margin_pct: Mapped[float | None] = mapped_column(Float)
    portfolio_margin_pct: Mapped[float | None] = mapped_column(Float)
    net_margin_pct: Mapped[float | None] = mapped_column(Float)
    snapshot_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)


class EvmSnapshot(Base):
    __tablename__ = "evm_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int | None] = mapped_column(ForeignKey("programs.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_value: Mapped[float] = mapped_column(Float, nullable=False)
    earned_value: Mapped[float] = mapped_column(Float, nullable=False)
    actual_cost: Mapped[float] = mapped_column(Float, nullable=False)
    percent_complete: Mapped[float | None] = mapped_column(Float)
    bac: Mapped[float | None] = mapped_column(Float)
    cpi: Mapped[float | None] = mapped_column(Float)
    spi: Mapped[float | None] = mapped_column(Float)
    eac: Mapped[float | None] = mapped_column(Float)
    tcpi: Mapped[float | None] = mapped_column(Float)
    vac: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)
