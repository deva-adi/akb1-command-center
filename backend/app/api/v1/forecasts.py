"""KPI forecast endpoint — thin wrapper around app/services/forecast.py.

Pulls the historical snapshots for a KPI + programme, runs the three
forecast primitives (linear trend, weighted moving average, exponential
smoothing), and returns the next 3 months projected. No persistence —
frontends can re-request whenever they like.
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import KpiDefinition, KpiSnapshot, Program
from app.services.forecast import (
    exponential_smoothing,
    linear_trend,
    weighted_moving_average,
)

router = APIRouter(prefix="/forecasts", tags=["forecasts"])


class ForecastSeries(BaseModel):
    label: str
    values: list[float]


class ForecastOut(BaseModel):
    kpi_code: str
    programme_code: str | None
    historical_dates: list[date]
    historical_values: list[float]
    horizon_months: int
    horizon_labels: list[str]
    series: list[ForecastSeries]


def _next_month_labels(last_date: date, horizon: int) -> list[str]:
    labels: list[str] = []
    year, month = last_date.year, last_date.month
    for _ in range(horizon):
        month += 1
        if month > 12:
            month = 1
            year += 1
        labels.append(f"{year:04d}-{month:02d}")
    return labels


@router.get("", response_model=ForecastOut)
async def build_forecast(
    kpi_code: str = Query(..., description="KPI code, e.g. CPI / MARGIN"),
    programme_code: str | None = Query(default=None),
    horizon: int = Query(default=3, ge=1, le=12),
    session: AsyncSession = Depends(get_session),
) -> ForecastOut:
    kpi = (
        await session.execute(
            select(KpiDefinition).where(KpiDefinition.code == kpi_code)
        )
    ).scalar_one_or_none()
    if kpi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI code not found"
        )

    program_id: int | None = None
    if programme_code is not None:
        programme = (
            await session.execute(
                select(Program).where(Program.code == programme_code)
            )
        ).scalar_one_or_none()
        if programme is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Programme code not found"
            )
        program_id = programme.id

    stmt = (
        select(KpiSnapshot)
        .where(KpiSnapshot.kpi_id == kpi.id)
        .order_by(KpiSnapshot.snapshot_date.asc())
    )
    if program_id is not None:
        stmt = stmt.where(KpiSnapshot.program_id == program_id)
    snapshots = (await session.execute(stmt)).scalars().all()

    if len(snapshots) == 0:
        return ForecastOut(
            kpi_code=kpi_code,
            programme_code=programme_code,
            historical_dates=[],
            historical_values=[],
            horizon_months=horizon,
            horizon_labels=[],
            series=[],
        )

    values = [s.value for s in snapshots]
    dates = [s.snapshot_date for s in snapshots]
    last_date = dates[-1]

    linear = linear_trend(values, horizon=horizon)
    wma = [weighted_moving_average(values, window=3)] * horizon
    exp = [exponential_smoothing(values, alpha=0.4)] * horizon

    return ForecastOut(
        kpi_code=kpi_code,
        programme_code=programme_code,
        historical_dates=dates,
        historical_values=values,
        horizon_months=horizon,
        horizon_labels=_next_month_labels(last_date, horizon),
        series=[
            ForecastSeries(label="Linear trend", values=linear),
            ForecastSeries(label="Weighted moving avg", values=wma),
            ForecastSeries(label="Exponential smoothing", values=exp),
        ],
    )
