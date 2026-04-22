from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ProgrammeRate(Base):
    """Per-programme, per-tier, per-month rate snapshot.

    Feeds Tab 12 P&L Cockpit pyramid economics and the Price and Mix drivers
    of the margin bridge. One row per (program_code, snapshot_date, role_tier).
    """

    __tablename__ = "programme_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    role_tier: Mapped[str] = mapped_column(String(20), nullable=False)
    planned_rate: Mapped[float] = mapped_column(Float, nullable=False)
    actual_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    planned_headcount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_headcount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tier_weight_planned: Mapped[float | None] = mapped_column(Float, nullable=True)
    tier_weight_actual: Mapped[float | None] = mapped_column(Float, nullable=True)
