from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging_config import get_logger
from app.models import (
    AiCodeMetrics,
    AiGovernanceConfig,
    AiOverrideLog,
    AiSdlcMetrics,
    AiTool,
    AiToolAssignment,
    AiTrustScore,
    AiUsageMetrics,
    AppSetting,
    AuditLog,
    BacklogItem,
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
    PhaseDeliverable,
    Program,
    Project,
    ProjectPhase,
    RateCard,
    ResourcePool,
    Risk,
    ScenarioExecution,
    ScopeCreepLog,
    SlaIncident,
    SprintData,
    SprintVelocityBlendRule,
    SprintVelocityDual,
)
from app.seed.ai_data import (
    AI_CODE_METRICS,
    AI_GOVERNANCE_CONFIG,
    AI_OVERRIDE_LOG,
    AI_SDLC_METRICS,
    AI_TOOL_ASSIGNMENTS,
    AI_TOOLS,
    AI_TRUST_SCORES,
    AI_USAGE_METRICS,
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
    BACKLOG_ITEMS,
    EVM_SNAPSHOTS,
    FLOW_METRICS,
    KANBAN_FLOW_ITEMS,
    MILESTONES,
    PHASE_DELIVERABLES,
    PROJECT_PHASES,
    SPRINTS,
    TTN_STORE_ITEMS,
)
from app.seed.pnl_seed import seed_pnl
from app.seed.bharat_data import (
    BHARAT_AI_CODE_METRICS,
    BHARAT_AI_OVERRIDE_LOG,
    BHARAT_AI_SDLC_METRICS,
    BHARAT_AI_TOOL_ASSIGNMENTS,
    BHARAT_AI_TRUST_SCORES,
    BHARAT_AI_USAGE_METRICS,
    BHARAT_BACKLOG_ITEMS,
    BHARAT_BLEND_RULES,
    BHARAT_CHANGE_REQUESTS,
    BHARAT_COMMERCIAL_SCENARIOS,
    BHARAT_CUSTOMER_ACTIONS,
    BHARAT_CUSTOMER_EXPECTATIONS,
    BHARAT_CUSTOMER_SATISFACTION,
    BHARAT_EVM_SNAPSHOTS,
    BHARAT_LOSS_EXPOSURE,
    BHARAT_MILESTONES,
    BHARAT_MONTH_STARTS,
    BHARAT_MONTHLY_KPI_VALUES,
    BHARAT_PHASE_DELIVERABLES,
    BHARAT_PROGRAMME,
    BHARAT_PROJECT_PHASES,
    BHARAT_PROJECTS,
    BHARAT_RATE_CARDS,
    BHARAT_RISKS,
    BHARAT_SLA_INCIDENTS,
    BHARAT_SPRINT_VELOCITY_DUAL,
    BHARAT_SPRINTS,
)
from app.seed.ops_data import (
    AUDIT_LOG,
    RESOURCE_POOL,
    SCENARIO_EXECUTIONS,
)
from app.seed.hercules_data import (
    HERC_BACKLOG_ITEMS,
    HERC_COMMERCIAL_SCENARIOS,
    HERC_EVM_SNAPSHOTS,
    HERC_FLOW_METRICS,
    HERC_MGT_FLOW_ITEMS,
    HERC_MILESTONES,
    HERC_MONTH_STARTS,
    HERC_MONTHLY_KPI_VALUES,
    HERC_PROGRAMME,
    HERC_PROJECTS,
    HERC_RISKS,
    HERC_SPRINTS,
)

log = get_logger(__name__)


async def _load_existing_programme_ids(session: AsyncSession) -> dict[str, int]:
    """Return {code: id} for every programme currently in the DB."""
    rows = (await session.execute(select(Program.code, Program.id))).all()
    return {code: pid for code, pid in rows}


async def seed_demo_data(session: AsyncSession, *, force: bool = False) -> bool:
    """Populate the NovaTech demo portfolio and run additive v5.7.0 seeds.

    Returns True if the base NovaTech + Hercules + BHARAT seed was inserted
    on this run. Returns False if the DB already contained programmes and
    ``force`` was not set. The Tab 12 P&L Cockpit seed (``seed_pnl``) runs
    unconditionally because it is fully idempotent and must land on every
    container start so legacy v5.6 volumes pick up the new rows on upgrade.
    """
    existing = (await session.execute(select(Program.id).limit(1))).first()
    if existing is not None and not force:
        log.info("seed.skip", reason="programmes_already_present")
        # Tab 12 seed is idempotent. Run it against the existing programmes
        # so a v5.6 volume upgrading to v5.7.0 gets the 252 programme_rates,
        # the 14 monthly_actuals rows, and the billing-column backfill.
        programme_ids = await _load_existing_programme_ids(session)
        if programme_ids:
            pnl_summary = await seed_pnl(session, programme_ids)
            await session.commit()
            log.info("seed.pnl_only", summary=pnl_summary)
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
    await _seed_backlog_items(session, project_ids)
    await _seed_flow_metrics(session, project_ids)
    await _seed_project_phases(session, project_ids)
    await _seed_evm_snapshots(session, program_ids, project_ids)
    await _seed_phase_deliverables(session, project_ids)
    await _seed_milestones(session, program_ids, project_ids)
    await _seed_sprint_velocity_dual(session, program_ids, project_ids)
    await _seed_blend_rules(session, program_ids)
    await _seed_commercial_scenarios(session, program_ids)
    await _seed_loss_exposure(session, program_ids)
    await _seed_rate_cards(session, program_ids)
    await _seed_change_requests(session, program_ids, project_ids)
    await _seed_customer_satisfaction(session, program_ids)
    await _seed_sla_incidents(session, program_ids)
    ai_tool_ids = await _seed_ai_tools(session)
    await _seed_ai_tool_assignments(session, program_ids, ai_tool_ids)
    await _seed_ai_usage_metrics(session, program_ids, ai_tool_ids)
    await _seed_ai_code_metrics(session, program_ids, project_ids)
    await _seed_ai_sdlc_metrics(session, program_ids)
    await _seed_ai_trust_scores(session, program_ids, ai_tool_ids)
    await _seed_ai_governance_config(session, program_ids)
    await _seed_ai_override_log(session, program_ids, project_ids, ai_tool_ids)
    await _seed_scenario_executions(session)
    await _seed_resource_pool(session, program_ids, project_ids)
    await _seed_audit_log(session)

    # ── Bharat Digital Spine programme (added v5.6 — fully Indian-themed) ──
    bharat_prog_ids = await _seed_bharat_programme(session)
    bharat_proj_ids = await _seed_bharat_projects(session, bharat_prog_ids)
    await _seed_bharat_kpis(session, bharat_prog_ids, kpi_ids)
    await _seed_bharat_risks(session, bharat_prog_ids)
    await _seed_bharat_sprints(session, bharat_prog_ids, bharat_proj_ids)
    await _seed_bharat_backlog(session, bharat_proj_ids)
    await _seed_bharat_phases(session, bharat_proj_ids)
    await _seed_bharat_phase_deliverables(session, bharat_proj_ids)
    await _seed_bharat_evm(session, bharat_prog_ids, bharat_proj_ids)
    await _seed_bharat_milestones(session, bharat_prog_ids, bharat_proj_ids)
    await _seed_bharat_commercial(session, bharat_prog_ids)
    await _seed_bharat_losses(session, bharat_prog_ids)
    await _seed_bharat_rate_cards(session, bharat_prog_ids)
    await _seed_bharat_change_requests(session, bharat_prog_ids, bharat_proj_ids)
    await _seed_bharat_dual_velocity(session, bharat_prog_ids, bharat_proj_ids)
    await _seed_bharat_blend_rules(session, bharat_prog_ids)
    await _seed_bharat_satisfaction(session, bharat_prog_ids)
    await _seed_bharat_expectations(session, bharat_prog_ids)
    await _seed_bharat_actions(session, bharat_prog_ids)
    await _seed_bharat_sla(session, bharat_prog_ids)
    await _seed_bharat_ai(session, bharat_prog_ids, bharat_proj_ids, ai_tool_ids)

    # ── Hercules programme (added in v5.3 — separate from base NovaTech seed) ──
    herc_prog_ids = await _seed_hercules_programme(session)
    herc_proj_ids = await _seed_hercules_projects(session, herc_prog_ids)
    await _seed_hercules_kpis(session, herc_prog_ids, kpi_ids)
    await _seed_hercules_risks(session, herc_prog_ids)
    await _seed_hercules_sprints(session, herc_prog_ids, herc_proj_ids)
    await _seed_hercules_backlog(session, herc_proj_ids)
    await _seed_hercules_flow(session, herc_proj_ids)
    await _seed_hercules_mgt_flow_items(session, herc_proj_ids)
    await _seed_hercules_evm(session, herc_proj_ids)
    await _seed_hercules_milestones(session, herc_proj_ids)
    await _seed_hercules_commercial(session, herc_prog_ids)

    # v5.7.0 Tab 12 P&L Cockpit seed (programme_rates, Feb-Mar monthly
    # actuals, billing-column backfill). Idempotent by construction.
    all_program_ids: dict[str, int] = {**program_ids, **herc_prog_ids, **bharat_prog_ids}
    pnl_summary = await seed_pnl(session, all_program_ids)
    log.info("seed.pnl", summary=pnl_summary)

    await session.commit()
    log.info(
        "seed.done",
        backlog_items=len(BACKLOG_ITEMS) + len(KANBAN_FLOW_ITEMS) + len(TTN_STORE_ITEMS),
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
        ai_tools=len(AI_TOOLS),
        ai_assignments=len(AI_TOOL_ASSIGNMENTS),
        ai_usage_rows=len(AI_USAGE_METRICS),
        ai_code_rows=len(AI_CODE_METRICS),
        ai_sdlc_rows=len(AI_SDLC_METRICS),
        ai_trust_rows=len(AI_TRUST_SCORES),
        ai_governance_rows=len(AI_GOVERNANCE_CONFIG),
        ai_overrides=len(AI_OVERRIDE_LOG),
        scenarios=len(SCENARIO_EXECUTIONS),
        resources=len(RESOURCE_POOL),
        audit_entries=len(AUDIT_LOG),
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


async def _seed_ai_tools(session: AsyncSession) -> dict[str, int]:
    tool_ids: dict[str, int] = {}
    for data in AI_TOOLS:
        tool = AiTool(**data)
        session.add(tool)
        await session.flush()
        tool_ids[tool.name] = tool.id
    return tool_ids


async def _seed_ai_tool_assignments(
    session: AsyncSession,
    program_ids: dict[str, int],
    tool_ids: dict[str, int],
) -> None:
    for data in AI_TOOL_ASSIGNMENTS:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        if tool_id is None or program_id is None:
            continue
        session.add(
            AiToolAssignment(
                ai_tool_id=tool_id, program_id=program_id, **payload
            )
        )


async def _seed_ai_usage_metrics(
    session: AsyncSession,
    program_ids: dict[str, int],
    tool_ids: dict[str, int],
) -> None:
    for data in AI_USAGE_METRICS:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        if tool_id is None or program_id is None:
            continue
        session.add(
            AiUsageMetrics(
                ai_tool_id=tool_id, program_id=program_id, **payload
            )
        )


async def _seed_ai_code_metrics(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in AI_CODE_METRICS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        project_id = project_ids.get(payload.pop("project_code"))
        if program_id is None or project_id is None:
            continue
        session.add(
            AiCodeMetrics(
                program_id=program_id, project_id=project_id, **payload
            )
        )


async def _seed_ai_sdlc_metrics(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in AI_SDLC_METRICS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(AiSdlcMetrics(program_id=program_id, **payload))


async def _seed_ai_trust_scores(
    session: AsyncSession,
    program_ids: dict[str, int],
    tool_ids: dict[str, int],
) -> None:
    for data in AI_TRUST_SCORES:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        if tool_id is None or program_id is None:
            continue
        session.add(
            AiTrustScore(
                ai_tool_id=tool_id, program_id=program_id, **payload
            )
        )


async def _seed_ai_governance_config(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in AI_GOVERNANCE_CONFIG:
        payload = dict(data)
        program_code = payload.pop("program_code", None)
        program_id = program_ids.get(program_code) if program_code else None
        session.add(AiGovernanceConfig(program_id=program_id, **payload))


async def _seed_ai_override_log(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
    tool_ids: dict[str, int],
) -> None:
    for data in AI_OVERRIDE_LOG:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        project_code = payload.pop("project_code", None)
        project_id = project_ids.get(project_code) if project_code else None
        session.add(
            AiOverrideLog(
                ai_tool_id=tool_id,
                program_id=program_id,
                project_id=project_id,
                **payload,
            )
        )


async def _seed_scenario_executions(session: AsyncSession) -> None:
    for data in SCENARIO_EXECUTIONS:
        session.add(ScenarioExecution(**data))


async def _seed_resource_pool(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in RESOURCE_POOL:
        payload = dict(data)
        program_code = payload.pop("current_program_code", None)
        project_code = payload.pop("current_project_code", None)
        session.add(
            ResourcePool(
                current_program_id=program_ids.get(program_code) if program_code else None,
                current_project_id=project_ids.get(project_code) if project_code else None,
                **payload,
            )
        )


async def _seed_backlog_items(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    all_items = list(BACKLOG_ITEMS) + list(KANBAN_FLOW_ITEMS) + list(TTN_STORE_ITEMS)
    for data in all_items:
        payload = dict(data)
        project_code = payload.pop("project_code")
        project_id = project_ids.get(project_code)
        if project_id is None:
            continue
        session.add(BacklogItem(project_id=project_id, **payload))


async def _seed_audit_log(session: AsyncSession) -> None:
    for data in AUDIT_LOG:
        session.add(AuditLog(**data))


# ── Hercules helpers ──────────────────────────────────────────────────────

async def _seed_hercules_programme(session: AsyncSession) -> dict[str, int]:
    programme = Program(**HERC_PROGRAMME)
    session.add(programme)
    await session.flush()
    return {programme.code: programme.id}


async def _seed_hercules_projects(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> dict[str, int]:
    project_ids: dict[str, int] = {}
    for data in HERC_PROJECTS:
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


async def _seed_hercules_kpis(
    session: AsyncSession,
    program_ids: dict[str, int],
    kpi_ids: dict[str, int],
) -> None:
    for (program_code, kpi_code), values in HERC_MONTHLY_KPI_VALUES.items():
        program_id = program_ids.get(program_code)
        kpi_id = kpi_ids.get(kpi_code)
        if program_id is None or kpi_id is None:
            continue
        for month_start, value in zip(HERC_MONTH_STARTS, values, strict=False):
            session.add(
                KpiSnapshot(
                    program_id=program_id,
                    kpi_id=kpi_id,
                    snapshot_date=month_start,
                    value=value,
                    trend=_trend_label(values),
                )
            )


async def _seed_hercules_risks(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in HERC_RISKS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(Risk(program_id=program_id, **payload))


async def _seed_hercules_sprints(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    herc_projects = {p["code"]: p["program_code"] for p in HERC_PROJECTS}
    for data in HERC_SPRINTS:
        payload = dict(data)
        project_code = payload.pop("project_code")
        project_id = project_ids.get(project_code)
        program_code = herc_projects.get(project_code)
        program_id = program_ids.get(program_code) if program_code else None
        if project_id is None:
            continue
        session.add(SprintData(program_id=program_id, project_id=project_id, **payload))


async def _seed_hercules_backlog(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in HERC_BACKLOG_ITEMS:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(BacklogItem(project_id=project_id, **payload))


async def _seed_hercules_flow(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in HERC_FLOW_METRICS:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(FlowMetrics(project_id=project_id, **payload))


async def _seed_hercules_commercial(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in HERC_COMMERCIAL_SCENARIOS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(CommercialScenario(program_id=program_id, **payload))


async def _seed_hercules_mgt_flow_items(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in HERC_MGT_FLOW_ITEMS:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(BacklogItem(project_id=project_id, **payload))


async def _seed_hercules_evm(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in HERC_EVM_SNAPSHOTS:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(EvmSnapshot(project_id=project_id, **payload))


async def _seed_hercules_milestones(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in HERC_MILESTONES:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(Milestone(project_id=project_id, **payload))


# ── Phase deliverables (base NovaTech — TTN-STORE) ───────────────────────

async def _seed_phase_deliverables(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    """Resolve (project_code, phase_name) to phase_id + project_id."""
    # First flush so the phase rows just added have IDs queryable.
    await session.flush()
    # Load the phases already inserted so we can map names to ids.
    from sqlalchemy import select as _select
    rows = (await session.execute(_select(ProjectPhase))).scalars().all()
    phase_key: dict[tuple[int, str], int] = {}
    for p in rows:
        if p.project_id is not None:
            phase_key[(p.project_id, p.phase_name)] = p.id

    for data in PHASE_DELIVERABLES:
        payload = dict(data)
        project_code = payload.pop("project_code")
        phase_name = payload.pop("phase_name")
        project_id = project_ids.get(project_code)
        if project_id is None:
            continue
        phase_id = phase_key.get((project_id, phase_name))
        if phase_id is None:
            continue
        session.add(
            PhaseDeliverable(
                phase_id=phase_id,
                project_id=project_id,
                **payload,
            )
        )


# ── Bharat helpers ───────────────────────────────────────────────────────

async def _seed_bharat_programme(session: AsyncSession) -> dict[str, int]:
    programme = Program(**BHARAT_PROGRAMME)
    session.add(programme)
    await session.flush()
    return {programme.code: programme.id}


async def _seed_bharat_projects(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> dict[str, int]:
    project_ids: dict[str, int] = {}
    for data in BHARAT_PROJECTS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        project = Project(program_id=program_id, **payload)
        session.add(project)
        await session.flush()
        project_ids[project.code] = project.id
    return project_ids


async def _seed_bharat_kpis(
    session: AsyncSession,
    program_ids: dict[str, int],
    kpi_ids: dict[str, int],
) -> None:
    for (program_code, kpi_code), values in BHARAT_MONTHLY_KPI_VALUES.items():
        program_id = program_ids.get(program_code)
        kpi_id = kpi_ids.get(kpi_code)
        if program_id is None or kpi_id is None:
            continue
        for month_start, value in zip(BHARAT_MONTH_STARTS, values, strict=False):
            session.add(
                KpiSnapshot(
                    program_id=program_id,
                    kpi_id=kpi_id,
                    snapshot_date=month_start,
                    value=value,
                    trend=_trend_label(values),
                )
            )


async def _seed_bharat_risks(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_RISKS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(Risk(program_id=program_id, **payload))


async def _seed_bharat_sprints(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    # Map project_code → program_code for Bharat projects.
    proj_to_prog = {p["code"]: p["program_code"] for p in BHARAT_PROJECTS}
    for data in BHARAT_SPRINTS:
        payload = dict(data)
        project_code = payload.pop("project_code")
        project_id = project_ids.get(project_code)
        program_code = proj_to_prog.get(project_code)
        program_id = program_ids.get(program_code) if program_code else None
        if project_id is None:
            continue
        session.add(SprintData(program_id=program_id, project_id=project_id, **payload))


async def _seed_bharat_backlog(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in BHARAT_BACKLOG_ITEMS:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(BacklogItem(project_id=project_id, **payload))


async def _seed_bharat_phases(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    for data in BHARAT_PROJECT_PHASES:
        payload = dict(data)
        project_id = project_ids.get(payload.pop("project_code"))
        if project_id is None:
            continue
        session.add(ProjectPhase(project_id=project_id, **payload))


async def _seed_bharat_phase_deliverables(
    session: AsyncSession,
    project_ids: dict[str, int],
) -> None:
    await session.flush()
    from sqlalchemy import select as _select
    rows = (await session.execute(
        _select(ProjectPhase).where(
            ProjectPhase.project_id.in_(list(project_ids.values()))
        )
    )).scalars().all()
    phase_key: dict[tuple[int, str], int] = {}
    for p in rows:
        if p.project_id is not None:
            phase_key[(p.project_id, p.phase_name)] = p.id

    for data in BHARAT_PHASE_DELIVERABLES:
        payload = dict(data)
        project_code = payload.pop("project_code")
        phase_name = payload.pop("phase_name")
        project_id = project_ids.get(project_code)
        if project_id is None:
            continue
        phase_id = phase_key.get((project_id, phase_name))
        if phase_id is None:
            continue
        session.add(
            PhaseDeliverable(
                phase_id=phase_id,
                project_id=project_id,
                **payload,
            )
        )


async def _seed_bharat_evm(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    proj_to_prog = {p["code"]: p["program_code"] for p in BHARAT_PROJECTS}
    for data in BHARAT_EVM_SNAPSHOTS:
        payload = dict(data)
        project_code = payload.pop("project_code")
        project_id = project_ids.get(project_code)
        program_code = proj_to_prog.get(project_code)
        program_id = program_ids.get(program_code) if program_code else None
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


async def _seed_bharat_milestones(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    proj_to_prog = {p["code"]: p["program_code"] for p in BHARAT_PROJECTS}
    for data in BHARAT_MILESTONES:
        payload = dict(data)
        project_code = payload.pop("project_code")
        project_id = project_ids.get(project_code)
        program_code = proj_to_prog.get(project_code)
        program_id = program_ids.get(program_code) if program_code else None
        if project_id is None:
            continue
        session.add(Milestone(program_id=program_id, project_id=project_id, **payload))


async def _seed_bharat_commercial(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_COMMERCIAL_SCENARIOS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(CommercialScenario(program_id=program_id, **payload))


async def _seed_bharat_losses(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_LOSS_EXPOSURE:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(LossExposure(program_id=program_id, **payload))


async def _seed_bharat_rate_cards(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_RATE_CARDS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(RateCard(program_id=program_id, **payload))


async def _seed_bharat_change_requests(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    for data in BHARAT_CHANGE_REQUESTS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        project_code = payload.pop("project_code", None)
        project_id = project_ids.get(project_code) if project_code else None
        if program_id is None:
            continue
        session.add(ScopeCreepLog(program_id=program_id, project_id=project_id, **payload))


async def _seed_bharat_dual_velocity(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
) -> None:
    proj_to_prog = {p["code"]: p["program_code"] for p in BHARAT_PROJECTS}
    for data in BHARAT_SPRINT_VELOCITY_DUAL:
        payload = dict(data)
        project_code = payload.pop("project_code")
        project_id = project_ids.get(project_code)
        program_code = proj_to_prog.get(project_code)
        program_id = program_ids.get(program_code) if program_code else None
        if project_id is None:
            continue
        session.add(
            SprintVelocityDual(
                program_id=program_id, project_id=project_id, **payload
            )
        )


async def _seed_bharat_blend_rules(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_BLEND_RULES:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(SprintVelocityBlendRule(program_id=program_id, **payload))


async def _seed_bharat_satisfaction(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_CUSTOMER_SATISFACTION:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(CustomerSatisfaction(program_id=program_id, **payload))


async def _seed_bharat_expectations(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_CUSTOMER_EXPECTATIONS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        expected = payload["expected_score"]
        delivered = payload["delivered_score"]
        if expected is not None and delivered is not None:
            payload["gap"] = delivered - expected
        session.add(CustomerExpectation(program_id=program_id, **payload))


async def _seed_bharat_actions(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_CUSTOMER_ACTIONS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(CustomerAction(program_id=program_id, **payload))


async def _seed_bharat_sla(
    session: AsyncSession,
    program_ids: dict[str, int],
) -> None:
    for data in BHARAT_SLA_INCIDENTS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(SlaIncident(program_id=program_id, **payload))


async def _seed_bharat_ai(
    session: AsyncSession,
    program_ids: dict[str, int],
    project_ids: dict[str, int],
    tool_ids: dict[str, int],
) -> None:
    for data in BHARAT_AI_TOOL_ASSIGNMENTS:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        if tool_id is None or program_id is None:
            continue
        session.add(
            AiToolAssignment(ai_tool_id=tool_id, program_id=program_id, **payload)
        )

    for data in BHARAT_AI_USAGE_METRICS:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        if tool_id is None or program_id is None:
            continue
        session.add(
            AiUsageMetrics(ai_tool_id=tool_id, program_id=program_id, **payload)
        )

    for data in BHARAT_AI_TRUST_SCORES:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        if tool_id is None or program_id is None:
            continue
        session.add(
            AiTrustScore(ai_tool_id=tool_id, program_id=program_id, **payload)
        )

    for data in BHARAT_AI_OVERRIDE_LOG:
        payload = dict(data)
        tool_id = tool_ids.get(payload.pop("tool_name"))
        program_id = program_ids.get(payload.pop("program_code"))
        project_code = payload.pop("project_code", None)
        project_id = project_ids.get(project_code) if project_code else None
        session.add(
            AiOverrideLog(
                ai_tool_id=tool_id,
                program_id=program_id,
                project_id=project_id,
                **payload,
            )
        )

    for data in BHARAT_AI_SDLC_METRICS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        if program_id is None:
            continue
        session.add(AiSdlcMetrics(program_id=program_id, **payload))

    for data in BHARAT_AI_CODE_METRICS:
        payload = dict(data)
        program_id = program_ids.get(payload.pop("program_code"))
        project_id = project_ids.get(payload.pop("project_code"))
        if program_id is None or project_id is None:
            continue
        session.add(
            AiCodeMetrics(program_id=program_id, project_id=project_id, **payload)
        )
