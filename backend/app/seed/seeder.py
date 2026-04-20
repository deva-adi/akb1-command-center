from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging_config import get_logger
from app.models import (
    AppSetting,
    CurrencyRate,
    KpiDefinition,
    KpiSnapshot,
    Program,
    Project,
    Risk,
)
from app.seed.data import (
    APP_SETTINGS_DEFAULTS,
    CURRENCY_RATES,
    KPI_DEFINITIONS,
    MONTH_STARTS,
    MONTHLY_KPI_VALUES,
    PROGRAMMES,
    PROJECTS,
    RISKS,
)

log = get_logger(__name__)


async def seed_demo_data(session: AsyncSession, *, force: bool = False) -> bool:
    """Populate the NovaTech demo portfolio.

    Returns True if seed data was inserted, False if the database already
    contained programmes and `force` was not set.
    """
    existing = (await session.execute(select(Program.id).limit(1))).first()
    if existing is not None and not force:
        log.info("seed.skip", reason="programmes_already_present")
        return False

    await _seed_app_settings(session)
    await _seed_currency_rates(session)
    program_ids = await _seed_programmes(session)
    await _seed_projects(session, program_ids)
    kpi_ids = await _seed_kpi_definitions(session)
    await _seed_kpi_snapshots(session, program_ids, kpi_ids)
    await _seed_risks(session, program_ids)

    await session.commit()
    log.info(
        "seed.done",
        programmes=len(program_ids),
        kpis=len(kpi_ids),
        risks=len(RISKS),
    )
    return True


async def _seed_app_settings(session: AsyncSession) -> None:
    for key, value in APP_SETTINGS_DEFAULTS.items():
        existing = await session.get(AppSetting, key)
        if existing is None:
            session.add(AppSetting(key=key, value=value))


async def _seed_currency_rates(session: AsyncSession) -> None:
    for code, symbol, rate in CURRENCY_RATES:
        existing = await session.get(CurrencyRate, code)
        if existing is None:
            session.add(
                CurrencyRate(
                    code=code,
                    symbol=symbol,
                    rate_to_base=Decimal(str(rate)),
                    source="seed",
                )
            )


async def _seed_programmes(session: AsyncSession) -> dict[str, int]:
    program_ids: dict[str, int] = {}
    for data in PROGRAMMES:
        programme = Program(**data)
        session.add(programme)
        await session.flush()
        program_ids[programme.code] = programme.id
    return program_ids


async def _seed_projects(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in PROJECTS:
        payload = dict(data)
        program_code = payload.pop("program_code")
        program_id = program_ids.get(program_code)
        if program_id is None:
            continue
        project = Project(program_id=program_id, **payload)
        session.add(project)


async def _seed_kpi_definitions(session: AsyncSession) -> dict[str, int]:
    kpi_ids: dict[str, int] = {}
    for data in KPI_DEFINITIONS:
        kpi = KpiDefinition(**data)
        session.add(kpi)
        await session.flush()
        kpi_ids[kpi.code] = kpi.id
    return kpi_ids


async def _seed_kpi_snapshots(
    session: AsyncSession,
    program_ids: dict[str, int],
    kpi_ids: dict[str, int],
) -> None:
    for (program_code, kpi_code), values in MONTHLY_KPI_VALUES.items():
        program_id = program_ids.get(program_code)
        kpi_id = kpi_ids.get(kpi_code)
        if program_id is None or kpi_id is None:
            continue
        for month_start, value in zip(MONTH_STARTS, values, strict=True):
            session.add(
                KpiSnapshot(
                    program_id=program_id,
                    kpi_id=kpi_id,
                    snapshot_date=month_start,
                    value=value,
                    trend=_trend_label(values),
                )
            )


def _trend_label(values: list[float]) -> str:
    if len(values) < 2:
        return "flat"
    if values[-1] > values[0]:
        return "up"
    if values[-1] < values[0]:
        return "down"
    return "flat"


async def _seed_risks(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in RISKS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(Risk(program_id=program_id, **payload))
