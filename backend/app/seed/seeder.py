from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging_config import get_logger
from app.models import (
    AppSetting,
    CommercialScenario,
    CurrencyRate,
    CustomerAction,
    CustomerExpectation,
    CustomerSatisfaction,
    EvmSnapshot,
    FlowMetrics,
    KpiDefinition,
    KpiSnapshot,
    LossExposure,
    Milestone,
    Program,
    Project,
    ProjectPhase,
    RateCard,
    Risk,
    ScopeCreepLog,
    SlaIncident,
    SprintData,
    SprintVelocityBlendRule,
    SprintVelocityDual,
)
from app.seed.commercial_data import (
    BLEND_RULES,
    CHANGE_REQUESTS,
    COMMERCIAL_SCENARIOS,
    LOSS_EXPOSURE,
    RATE_CARDS,
    SPRINT_VELOCITY_DUAL,
)
from app.seed.customer_data import CUSTOMER_SATISFACTION, SLA_INCIDENTS
from app.seed.data import (
    APP_SETTINGS_DEFAULTS,
    CURRENCY_RATES,
    CUSTOMER_ACTIONS,
    CUSTOMER_EXPECTATIONS,
    KPI_DEFINITIONS,
    MONTH_STARTS,
    MONTHLY_KPI_VALUES,
    PROGRAMMES,
    PROJECTS,
    RISKS,
)
from app.seed.delivery_data import (
    EVM_SNAPSHOTS,
    FLOW_METRICS,
    MILESTONES,
    PROJECT_PHASES,
    SPRINTS,
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
    project_ids = await _seed_projects(session, program_ids)
    kpi_ids = await _seed_kpi_definitions(session)
    await _seed_kpi_snapshots(session, program_ids, kpi_ids)
    await _seed_risks(session, program_ids)
    await _seed_customer_expectations(session, program_ids)
    await _seed_customer_actions(session, program_ids)
    await _seed_sprints(session, program_ids, project_ids)
    await _seed_flow_metrics(session, project_ids)
    await _seed_project_phases(session, project_ids)
    await _seed_evm_snapshots(session, program_ids, project_ids)
    await _seed_milestones(session, program_ids, project_ids)
    await _seed_sprint_velocity_dual(session, program_ids, project_ids)
    await _seed_blend_rules(session, program_ids)
    await _seed_commercial_scenarios(session, program_ids)
    await _seed_loss_exposure(session, program_ids)
    await _seed_rate_cards(session, program_ids)
    await _seed_change_requests(session, program_ids, project_ids)
    await _seed_customer_satisfaction(session, program_ids)
    await _seed_sla_incidents(session, program_ids)

    await session.commit()
    log.info(
        "seed.done",
        programmes=len(program_ids),
        projects=len(project_ids),
        kpis=len(kpi_ids),
        risks=len(RISKS),
        expectations=len(CUSTOMER_EXPECTATIONS),
        actions=len(CUSTOMER_ACTIONS),
        sprints=len(SPRINTS),
        flow_rows=len(FLOW_METRICS),
        phases=len(PROJECT_PHASES),
        evm_rows=len(EVM_SNAPSHOTS),
        milestones=len(MILESTONES),
        dual_velocity=len(SPRINT_VELOCITY_DUAL),
        blend_rules=len(BLEND_RULES),
        commercial=len(COMMERCIAL_SCENARIOS),
        losses=len(LOSS_EXPOSURE),
        rate_cards=len(RATE_CARDS),
        change_requests=len(CHANGE_REQUESTS),
        customer_satisfaction=len(CUSTOMER_SATISFACTION),
        sla_incidents=len(SLA_INCIDENTS),
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
) -> dict[str, int]:
    project_ids: dict[str, int] = {}
    for data in PROJECTS:
        payload = dict(data)
        program_code = payload.pop("program_code")
        program_id = program_ids.get(program_code)
        if program_id is None:
            continue
        project = Project(program_id=program_id, **payload)
        session.add(project)
        await session.flush()
        project_ids[project.code] = project.id
    return project_ids


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


async def _seed_customer_expectations(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in CUSTOMER_EXPECTATIONS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        expected = payload["expected_score"]
        delivered = payload["delivered_score"]
        if expected is not None and delivered is not None:
            payload["gap"] = delivered - expected
        session.add(CustomerExpectation(program_id=program_id, **payload))


async def _seed_customer_actions(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in CUSTOMER_ACTIONS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(CustomerAction(program_id=program_id, **payload))


def _program_for_project(
    project_code: str,
    project_ids: dict[str, int],
    program_ids: dict[str, int],
) -> tuple[int | None, int | None]:
    """Return (program_id, project_id) for a project code; None if unknown."""
    project_id = project_ids.get(project_code)
    if project_id is None:
        return None, None
    # Reverse-map project_code → program_code via the PROJECTS source table.
    for seed in PROJECTS:
        if seed["code"] == project_code:
            return program_ids.get(seed["program_code"]), project_id
    return None, project_id


async def _seed_sprints(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in SPRINTS:
        payload = dict(data)
        project_code = payload.pop("project_code")
        program_id, project_id = _program_for_project(
            project_code, project_ids, program_ids
        )
        if project_id is None:
            continue
        session.add(
            SprintData(program_id=program_id, project_id=project_id, **payload)
        )


async def _seed_flow_metrics(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in FLOW_METRICS:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(FlowMetrics(project_id=project_id, **payload))


async def _seed_project_phases(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in PROJECT_PHASES:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(ProjectPhase(project_id=project_id, **payload))


async def _seed_evm_snapshots(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in EVM_SNAPSHOTS:
        payload = dict(data)
        project_code = payload.pop("project_code")
        program_id, project_id = _program_for_project(
            project_code, project_ids, program_ids
        )
        if project_id is None:
            continue
        pv = payload["planned_value"]
        ev = payload["earned_value"]
        ac = payload["actual_cost"]
        bac = payload["bac"]
        payload["cpi"] = round(ev / ac, 4) if ac else None
        payload["spi"] = round(ev / pv, 4) if pv else None
        payload["eac"] = round(bac / payload["cpi"], 2) if payload["cpi"] else None
        payload["tcpi"] = (
            round((bac - ev) / (bac - ac), 4) if (bac - ac) > 0 else None
        )
        payload["vac"] = round(bac - payload["eac"], 2) if payload["eac"] else None
        session.add(
            EvmSnapshot(program_id=program_id, project_id=project_id, **payload)
        )


async def _seed_milestones(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in MILESTONES:
        payload = dict(data)
        project_code = payload.pop("project_code")
        program_id, project_id = _program_for_project(
            project_code, project_ids, program_ids
        )
        if project_id is None:
            continue
        session.add(
            Milestone(program_id=program_id, project_id=project_id, **payload)
        )


async def _seed_sprint_velocity_dual(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in SPRINT_VELOCITY_DUAL:
        payload = dict(data)
        project_code = payload.pop("project_code")
        program_id, project_id = _program_for_project(
            project_code, project_ids, program_ids
        )
        if project_id is None:
            continue
        session.add(
            SprintVelocityDual(
                program_id=program_id, project_id=project_id, **payload
            )
        )


async def _seed_blend_rules(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BLEND_RULES:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(SprintVelocityBlendRule(program_id=program_id, **payload))


async def _seed_commercial_scenarios(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in COMMERCIAL_SCENARIOS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(CommercialScenario(program_id=program_id, **payload))


async def _seed_loss_exposure(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in LOSS_EXPOSURE:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(LossExposure(program_id=program_id, **payload))


async def _seed_rate_cards(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in RATE_CARDS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(RateCard(program_id=program_id, **payload))


async def _seed_change_requests(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in CHANGE_REQUESTS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        project_code = payload.pop("project_code", None)
        project_id = project_ids.get(project_code) if project_code else None
        if program_id is None:
            continue
        session.add(
            ScopeCreepLog(program_id=program_id, project_id=project_id, **payload)
        )


async def _seed_customer_satisfaction(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in CUSTOMER_SATISFACTION:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(CustomerSatisfaction(program_id=program_id, **payload))


async def _seed_sla_incidents(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in SLA_INCIDENTS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(SlaIncident(program_id=program_id, **payload))
