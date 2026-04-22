"""P&L Cockpit endpoints for v5.7.0 Tab 12.

Nine endpoints under /api/v1/pnl. First two land in M3b-mid-checkpoint;
the remaining seven follow in the rest of M3b.

Shared-infra contract on every endpoint:

- Universal filter set parsed via ``pnl_filters_dependency``.
- ``filters_applied`` block echoes the resolved canonical filter set.
- ``lineage`` block names the formula and lists contributing rows.
- Non-2xx responses flow through ``install_error_handlers`` so every
  error carries the standard envelope.
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.pnl_filters import PnlFilters, pnl_filters_dependency
from app.database import get_session
from app.models import (
    CommercialScenario,
    EvmSnapshot,
    LossExposure,
    Program,
    ProgrammeRate,
    ResourcePool,
)
from app.schemas.pnl import (
    BridgeDriversOut,
    BridgeOut,
    DsoOut,
    EvmOut,
    FiltersApplied,
    LineageAtomicRow,
    LineageBlock,
    LineageEntry,
    LineageResolverOut,
    LossRow,
    LossesOut,
    PfaOut,
    PfaPoint,
    PfaSeries,
    PyramidOut,
    PyramidTier,
    RevenueCard,
    RevenueOut,
    WaterfallLayerOut,
    WaterfallOut,
)
from app.services.lineage_keys import parse as parse_lineage_key
from app.services.pnl_engine import (
    CommercialSnapshot,
    TierSnapshot,
    compute_bridge,
    compute_waterfall,
)

router = APIRouter(prefix="/pnl", tags=["pnl"])


# --- helpers ------------------------------------------------------------


def _filters_applied_from(filters: PnlFilters) -> FiltersApplied:
    """Build the canonical FiltersApplied response block."""
    return FiltersApplied.model_validate(filters.to_applied_block())


async def _lookup_programme(session: AsyncSession, code: str) -> Program | None:
    stmt = select(Program).where(Program.code == code.upper())
    return (await session.execute(stmt)).scalar_one_or_none()


async def _latest_commercial_for(
    session: AsyncSession,
    program_id: int,
    filters: PnlFilters,
    default_scenario: str = "Monthly Actuals",
) -> CommercialScenario | None:
    """Pick the latest scenario row for a programme under the given filters."""
    scenario_name = filters.scenario_name or default_scenario
    stmt = (
        select(CommercialScenario)
        .where(CommercialScenario.program_id == program_id)
        .where(CommercialScenario.scenario_name == scenario_name)
    )
    if filters.date_from is not None:
        stmt = stmt.where(CommercialScenario.snapshot_date >= filters.date_from)
    if filters.date_to is not None:
        stmt = stmt.where(CommercialScenario.snapshot_date <= filters.date_to)
    stmt = stmt.order_by(CommercialScenario.snapshot_date.desc())
    return (await session.execute(stmt)).scalars().first()


def _commercial_to_snapshot(row: CommercialScenario) -> CommercialSnapshot:
    return CommercialSnapshot(
        actual_revenue=float(row.actual_revenue or 0.0),
        actual_cost=float(row.actual_cost or 0.0),
        gross_margin_pct=float(row.gross_margin_pct or 0.0),
        contribution_margin_pct=(
            float(row.contribution_margin_pct) if row.contribution_margin_pct is not None else None
        ),
        portfolio_margin_pct=(
            float(row.portfolio_margin_pct) if row.portfolio_margin_pct is not None else None
        ),
        net_margin_pct=(float(row.net_margin_pct) if row.net_margin_pct is not None else None),
    )


def _rate_rows_to_snapshots(rows: list[ProgrammeRate]) -> list[TierSnapshot]:
    return [
        TierSnapshot(
            role_tier=r.role_tier,
            planned_rate=float(r.planned_rate),
            actual_rate=float(r.actual_rate or r.planned_rate),
            tier_weight_planned=float(r.tier_weight_planned or 0.0),
            tier_weight_actual=float(r.tier_weight_actual or 0.0),
        )
        for r in rows
    ]


async def _fetch_tier_rates(
    session: AsyncSession, program_code: str, snapshot_date: date
) -> list[ProgrammeRate]:
    stmt = (
        select(ProgrammeRate)
        .where(ProgrammeRate.program_code == program_code)
        .where(ProgrammeRate.snapshot_date == snapshot_date)
        .order_by(ProgrammeRate.role_tier)
    )
    return list((await session.execute(stmt)).scalars().all())


# --- endpoint 1: waterfall ---------------------------------------------


@router.get(
    "/waterfall/{programme_code}",
    response_model=WaterfallOut,
    response_model_by_alias=True,
    summary="Four-layer margin waterfall for a programme",
)
async def waterfall(
    programme_code: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> WaterfallOut:
    """Return the four-layer margin waterfall (Gross, Contribution, Portfolio, Net).

    Reads the latest ``commercial_scenarios`` row for ``programme_code``
    under the active filters. ``from``/``to`` narrow the date window;
    ``scenario_name`` defaults to ``Monthly Actuals``. The response carries
    a ``lineage`` block naming the source row and the four layer formulas.
    Returns HTTP 200 with ``layers=[]`` and ``revenue=0.0`` if no row
    matches the filters, keeping the envelope shape consistent for the
    frontend ContextRail.
    """
    code = programme_code.upper()
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    row = await _latest_commercial_for(session, programme.id, filters)
    applied = _filters_applied_from(filters)

    if row is None:
        return WaterfallOut(
            programme_code=code,
            snapshot_date=filters.date_to or filters.date_from or date(1970, 1, 1),
            scenario_name=filters.scenario_name or "Monthly Actuals",
            revenue=0.0,
            layers=[],
            filters_applied=applied,
            lineage=LineageBlock(
                formula="no matching commercial_scenarios row under active filters",
                formula_ref="PRD section 6.1 revenue+margin cards",
                entries=[],
                entries_total_count=0,
                sampling="full",
            ),
        )

    breakdown = compute_waterfall(_commercial_to_snapshot(row))
    layers_out = [
        WaterfallLayerOut(
            layer=layer.layer,
            label=layer.label,
            margin_pct=layer.margin_pct,
            margin_value=layer.margin_value,
        )
        for layer in breakdown.layers
    ]

    lineage_entry = LineageEntry(
        composite_key=f"{code}|{row.snapshot_date.isoformat()}|{row.scenario_name}|commercial_scenarios",
        program_code=code,
        snapshot_date=row.snapshot_date,
        scenario_name=row.scenario_name,
        table="commercial_scenarios",
        row_id=row.id,
        columns_used={
            "actual_revenue": float(row.actual_revenue or 0.0),
            "actual_cost": float(row.actual_cost or 0.0),
            "gross_margin_pct": float(row.gross_margin_pct or 0.0),
            "contribution_margin_pct": (
                float(row.contribution_margin_pct) if row.contribution_margin_pct is not None else None
            ),
            "portfolio_margin_pct": (
                float(row.portfolio_margin_pct) if row.portfolio_margin_pct is not None else None
            ),
            "net_margin_pct": (
                float(row.net_margin_pct) if row.net_margin_pct is not None else None
            ),
        },
        description=(
            "Four margin layers read directly from the commercial_scenarios row; "
            "margin_value = margin_pct * actual_revenue per layer."
        ),
    )
    lineage = LineageBlock(
        formula=(
            "Gross = (actual_revenue - actual_cost) / actual_revenue. "
            "Contribution, Portfolio, Net read directly from commercial_scenarios."
        ),
        formula_ref="PRD section 6.1 cards 7-10 and FORMULAS.md entries 14-17",
        entries=[lineage_entry],
        entries_total_count=1,
        sampling="full",
    )

    return WaterfallOut(
        programme_code=code,
        snapshot_date=row.snapshot_date,
        scenario_name=row.scenario_name,
        revenue=breakdown.revenue,
        layers=layers_out,
        filters_applied=applied,
        lineage=lineage,
    )


# --- endpoint 2: bridge ------------------------------------------------


@router.get(
    "/bridge/{metric_key}",
    response_model=BridgeOut,
    response_model_by_alias=True,
    summary="Margin bridge decomposition (Price, Volume, Mix, Cost) between two snapshots",
)
async def bridge(
    metric_key: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> BridgeOut:
    """Decompose a gross-margin delta between a prior and a current snapshot.

    Path parameter ``metric_key`` is a lineage key (see docs/LINEAGE_KEYS.md).
    Only ``{tab}.gross_margin_pct.programme.*`` keys are supported in v5.7.0;
    other metrics return 422 with a clear message so future work can add
    them without breaking callers.

    Required filters for this endpoint:

    - ``programme`` with exactly one programme code
    - ``from`` (prior snapshot date)
    - ``to`` (current snapshot date)

    Cost is the residual by construction. The four drivers always sum
    exactly to ``total_delta_bps``. ``total_delta_bps`` itself is computed
    from ``gross_margin_pct`` directly on the seed so it reconciles to
    the M2 reconciliation gate (Phoenix Feb to Mar = -340 bps).
    """
    parsed = parse_lineage_key(metric_key)
    if parsed.metric != "gross_margin_pct":
        raise HTTPException(
            status_code=422,
            detail=(
                f"bridge currently supports metric 'gross_margin_pct'; "
                f"received '{parsed.metric}' from metric_key '{metric_key}'"
            ),
        )

    if not filters.programmes or len(filters.programmes) != 1:
        raise HTTPException(
            status_code=400,
            detail="bridge requires exactly one programme code via the 'programme' filter",
        )
    if filters.date_from is None or filters.date_to is None:
        raise HTTPException(
            status_code=400,
            detail="bridge requires both 'from' and 'to' filters",
        )
    if filters.date_from >= filters.date_to:
        raise HTTPException(
            status_code=400,
            detail="'from' must be strictly earlier than 'to'",
        )

    code = filters.programmes[0]
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    scenario_name = filters.scenario_name or "Monthly Actuals"

    async def _scenario_at(snapshot_date: date) -> CommercialScenario | None:
        stmt = (
            select(CommercialScenario)
            .where(CommercialScenario.program_id == programme.id)
            .where(CommercialScenario.scenario_name == scenario_name)
            .where(CommercialScenario.snapshot_date == snapshot_date)
        )
        return (await session.execute(stmt)).scalar_one_or_none()

    prior_row = await _scenario_at(filters.date_from)
    current_row = await _scenario_at(filters.date_to)
    if prior_row is None or current_row is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"no commercial_scenarios rows for '{code}' at both {filters.date_from} "
                f"and {filters.date_to} under scenario '{scenario_name}'"
            ),
        )

    tiers_prior = _rate_rows_to_snapshots(
        await _fetch_tier_rates(session, code, filters.date_from)
    )
    tiers_current = _rate_rows_to_snapshots(
        await _fetch_tier_rates(session, code, filters.date_to)
    )

    breakdown = compute_bridge(
        prior=_commercial_to_snapshot(prior_row),
        current=_commercial_to_snapshot(current_row),
        tiers_prior=tiers_prior,
        tiers_current=tiers_current,
    )

    applied = _filters_applied_from(filters)

    lineage_entries = [
        LineageEntry(
            composite_key=f"{code}|{prior_row.snapshot_date.isoformat()}|{scenario_name}|commercial_scenarios",
            program_code=code,
            snapshot_date=prior_row.snapshot_date,
            scenario_name=scenario_name,
            table="commercial_scenarios",
            row_id=prior_row.id,
            columns_used={"gross_margin_pct": float(prior_row.gross_margin_pct or 0.0), "actual_revenue": float(prior_row.actual_revenue or 0.0)},
            description="prior snapshot for margin bridge",
        ),
        LineageEntry(
            composite_key=f"{code}|{current_row.snapshot_date.isoformat()}|{scenario_name}|commercial_scenarios",
            program_code=code,
            snapshot_date=current_row.snapshot_date,
            scenario_name=scenario_name,
            table="commercial_scenarios",
            row_id=current_row.id,
            columns_used={"gross_margin_pct": float(current_row.gross_margin_pct or 0.0), "actual_revenue": float(current_row.actual_revenue or 0.0)},
            description="current snapshot for margin bridge",
        ),
    ]
    for tier_row in tiers_prior + tiers_current:
        label = "prior" if tier_row in tiers_prior else "current"
        lineage_entries.append(
            LineageEntry(
                composite_key=f"{code}|{filters.date_from if label == 'prior' else filters.date_to}|{tier_row.role_tier}|programme_rates",
                program_code=code,
                snapshot_date=filters.date_from if label == "prior" else filters.date_to,
                scenario_name=None,
                table="programme_rates",
                row_id=None,
                columns_used={
                    "role_tier": tier_row.role_tier,
                    "planned_rate": tier_row.planned_rate,
                    "actual_rate": tier_row.actual_rate,
                    "tier_weight_actual": tier_row.tier_weight_actual,
                },
                description=f"{label} tier snapshot for Price and Mix drivers",
            )
        )

    lineage = LineageBlock(
        formula=(
            "Total delta bps = (current.gross_margin_pct - prior.gross_margin_pct) * 10000. "
            "Price, Volume, Mix approximate the rate, revenue, and tier-weight shift "
            "contributions. Cost is the residual so the four drivers always sum to total."
        ),
        formula_ref="PRD section 6.2 and FORMULAS.md entries 50 to 53",
        entries=lineage_entries,
        entries_total_count=len(lineage_entries),
        sampling="full",
    )

    return BridgeOut(
        metric_key=metric_key,
        programme_code=code,
        prior_snapshot_date=prior_row.snapshot_date,
        current_snapshot_date=current_row.snapshot_date,
        prior_value=breakdown.prior_value,
        current_value=breakdown.current_value,
        total_delta_bps=breakdown.total_delta_bps,
        drivers=BridgeDriversOut(
            price_bps=breakdown.drivers.price_bps,
            volume_bps=breakdown.drivers.volume_bps,
            mix_bps=breakdown.drivers.mix_bps,
            cost_bps_residual=breakdown.drivers.cost_bps_residual,
        ),
        filters_applied=applied,
        lineage=lineage,
    )


# --- endpoint 3: pfa ---------------------------------------------------


_PFA_METRICS = {"revenue", "gross_pct", "net_pct", "cpi", "spi"}


@router.get(
    "/pfa/{programme_code}",
    response_model=PfaOut,
    response_model_by_alias=True,
    summary="Plan, Forecast, Actual triangle per programme",
)
async def pfa(
    programme_code: str,
    metric: str = "gross_pct",
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> PfaOut:
    """Return three time series for a programme: Plan, Forecast, Actual.

    Plan is sourced from ``commercial_scenarios.planned_revenue`` and
    ``planned_cost``. Forecast is the ``scenario_name = 'Forecast at
    Completion'`` rows. Actual is the ``scenario_name = 'Monthly Actuals'``
    or ``'Quarterly Actuals'`` rows. CPI and SPI pull from
    ``evm_snapshots`` instead. Metric values are ``revenue``, ``gross_pct``,
    ``net_pct``, ``cpi``, ``spi``; anything else returns 422.
    """
    if metric not in _PFA_METRICS:
        raise HTTPException(
            status_code=422,
            detail=f"metric '{metric}' not supported; allowed: {sorted(_PFA_METRICS)}",
        )

    code = programme_code.upper()
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    plan: list[PfaPoint] = []
    forecast: list[PfaPoint] = []
    actual: list[PfaPoint] = []
    lineage_entries: list[LineageEntry] = []

    if metric in {"cpi", "spi"}:
        stmt = select(EvmSnapshot).where(EvmSnapshot.program_id == programme.id)
        if filters.date_from is not None:
            stmt = stmt.where(EvmSnapshot.snapshot_date >= filters.date_from)
        if filters.date_to is not None:
            stmt = stmt.where(EvmSnapshot.snapshot_date <= filters.date_to)
        stmt = stmt.order_by(EvmSnapshot.snapshot_date)
        rows = (await session.execute(stmt)).scalars().all()
        for row in rows:
            value = float(row.cpi) if metric == "cpi" and row.cpi is not None else (
                float(row.spi) if metric == "spi" and row.spi is not None else None
            )
            if value is not None and row.snapshot_date:
                actual.append(PfaPoint(snapshot_date=row.snapshot_date, value=value))
                lineage_entries.append(
                    LineageEntry(
                        composite_key=f"{code}|{row.snapshot_date.isoformat()}|evm_snapshots",
                        program_code=code,
                        snapshot_date=row.snapshot_date,
                        table="evm_snapshots",
                        row_id=row.id,
                        columns_used={metric: value},
                        description=f"{metric} at snapshot",
                    )
                )
    else:
        stmt = select(CommercialScenario).where(CommercialScenario.program_id == programme.id)
        if filters.date_from is not None:
            stmt = stmt.where(CommercialScenario.snapshot_date >= filters.date_from)
        if filters.date_to is not None:
            stmt = stmt.where(CommercialScenario.snapshot_date <= filters.date_to)
        stmt = stmt.order_by(CommercialScenario.snapshot_date)
        rows = (await session.execute(stmt)).scalars().all()

        def _value_for(row: CommercialScenario) -> float | None:
            if metric == "revenue":
                return float(row.actual_revenue) if row.actual_revenue is not None else None
            if metric == "gross_pct":
                return (
                    float(row.gross_margin_pct) if row.gross_margin_pct is not None else None
                )
            if metric == "net_pct":
                return float(row.net_margin_pct) if row.net_margin_pct is not None else None
            return None

        def _plan_value_for(row: CommercialScenario) -> float | None:
            if metric == "revenue":
                return float(row.planned_revenue) if row.planned_revenue is not None else None
            if metric in {"gross_pct", "net_pct"}:
                # Plan margin derived from planned_revenue and planned_cost.
                pr = row.planned_revenue
                pc = row.planned_cost
                if pr is None or pc is None or float(pr) == 0:
                    return None
                return (float(pr) - float(pc)) / float(pr)
            return None

        for row in rows:
            if row.snapshot_date is None:
                continue
            composite = f"{code}|{row.snapshot_date.isoformat()}|{row.scenario_name}|commercial_scenarios"
            v = _value_for(row)
            pv = _plan_value_for(row)
            scenario = (row.scenario_name or "").strip()
            if scenario in {"Monthly Actuals", "Quarterly Actuals"}:
                actual.append(PfaPoint(snapshot_date=row.snapshot_date, value=v))
            elif scenario == "Forecast at Completion":
                forecast.append(PfaPoint(snapshot_date=row.snapshot_date, value=v))
            if pv is not None:
                plan.append(PfaPoint(snapshot_date=row.snapshot_date, value=pv))
            lineage_entries.append(
                LineageEntry(
                    composite_key=composite,
                    program_code=code,
                    snapshot_date=row.snapshot_date,
                    scenario_name=row.scenario_name,
                    table="commercial_scenarios",
                    row_id=row.id,
                    columns_used={"metric": metric, "value": v, "plan_value": pv},
                    description=f"{scenario} row feeding {metric} series",
                )
            )

    applied = _filters_applied_from(filters)
    lineage = LineageBlock(
        formula=(
            f"PFA triangle for metric='{metric}'. Plan from planned_revenue/"
            "planned_cost, Forecast from 'Forecast at Completion' scenario, "
            "Actual from 'Monthly Actuals' or 'Quarterly Actuals'. CPI and SPI "
            "read from evm_snapshots."
        ),
        formula_ref="PRD section 6.3 and FORMULAS.md entries 7, 13, 14, 17",
        entries=lineage_entries,
        entries_total_count=len(lineage_entries),
        sampling="full",
    )
    return PfaOut(
        programme_code=code,
        metric=metric,  # type: ignore[arg-type]
        series=PfaSeries(plan=plan, forecast=forecast, actual=actual),
        filters_applied=applied,
        lineage=lineage,
    )


# --- endpoint 4: pyramid -----------------------------------------------


def _pyramid_rag(planned: dict[str, float], actual: dict[str, float]) -> str:
    """Simple RAG: green if max weight delta <= 5pp, amber <= 15pp, else red."""
    if not planned or not actual:
        return "amber"
    deltas = [abs(actual.get(k, 0.0) - v) for k, v in planned.items()]
    max_delta = max(deltas) * 100 if deltas else 0.0
    if max_delta <= 5:
        return "green"
    if max_delta <= 15:
        return "amber"
    return "red"


@router.get(
    "/pyramid/{programme_code}",
    response_model=PyramidOut,
    response_model_by_alias=True,
    summary="Pyramid ratio, weights, headcount, utilisation per tier",
)
async def pyramid(
    programme_code: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> PyramidOut:
    """Return per-tier pyramid data for a programme.

    Reads the latest ``programme_rates`` row per tier (filtered by
    ``month`` or ``from``/``to``) and augments each tier with utilisation
    sourced from ``resource_pool`` for that programme. RAG classifies
    the largest planned-vs-actual weight delta across tiers.
    """
    code = programme_code.upper()
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    stmt = select(ProgrammeRate).where(ProgrammeRate.program_code == code)
    if filters.month is not None:
        stmt = stmt.where(ProgrammeRate.snapshot_date == filters.month)
    else:
        if filters.date_from is not None:
            stmt = stmt.where(ProgrammeRate.snapshot_date >= filters.date_from)
        if filters.date_to is not None:
            stmt = stmt.where(ProgrammeRate.snapshot_date <= filters.date_to)
    stmt = stmt.order_by(ProgrammeRate.snapshot_date.desc(), ProgrammeRate.role_tier)
    rows = list((await session.execute(stmt)).scalars().all())

    # Pick the latest snapshot_date present in the window.
    latest_date: date | None = rows[0].snapshot_date if rows else None
    latest_rows = [r for r in rows if r.snapshot_date == latest_date] if latest_date else []

    # Utilisation from resource_pool averaged per tier.
    util_stmt = select(ResourcePool).where(ResourcePool.current_program_id == programme.id)
    util_rows = (await session.execute(util_stmt)).scalars().all()
    util_by_tier: dict[str, float] = {}
    count_by_tier: dict[str, int] = {}
    for r in util_rows:
        tier = (r.role_tier or "").strip()
        if tier not in {"Junior", "Mid", "Senior"}:
            continue
        if r.utilization_pct is None:
            continue
        util_by_tier[tier] = util_by_tier.get(tier, 0.0) + float(r.utilization_pct)
        count_by_tier[tier] = count_by_tier.get(tier, 0) + 1
    for tier in list(util_by_tier.keys()):
        util_by_tier[tier] = round(util_by_tier[tier] / count_by_tier[tier], 2)

    tiers_out: list[PyramidTier] = []
    planned_weights: dict[str, float] = {}
    actual_weights: dict[str, float] = {}
    lineage_entries: list[LineageEntry] = []
    for r in latest_rows:
        tier_name = r.role_tier if r.role_tier in {"Junior", "Mid", "Senior"} else None
        if tier_name is None:
            continue
        planned_weights[tier_name] = float(r.tier_weight_planned or 0.0)
        actual_weights[tier_name] = float(r.tier_weight_actual or 0.0)
        tiers_out.append(
            PyramidTier(
                role_tier=tier_name,  # type: ignore[arg-type]
                planned_headcount=r.planned_headcount,
                actual_headcount=r.actual_headcount,
                planned_weight=float(r.tier_weight_planned) if r.tier_weight_planned is not None else None,
                actual_weight=float(r.tier_weight_actual) if r.tier_weight_actual is not None else None,
                planned_rate=float(r.planned_rate),
                actual_rate=float(r.actual_rate) if r.actual_rate is not None else None,
                utilisation_pct=util_by_tier.get(tier_name),
            )
        )
        lineage_entries.append(
            LineageEntry(
                composite_key=f"{code}|{r.snapshot_date.isoformat()}|{tier_name}|programme_rates",
                program_code=code,
                snapshot_date=r.snapshot_date,
                table="programme_rates",
                row_id=r.id,
                columns_used={
                    "role_tier": tier_name,
                    "planned_rate": float(r.planned_rate),
                    "actual_rate": float(r.actual_rate) if r.actual_rate is not None else None,
                    "tier_weight_planned": float(r.tier_weight_planned or 0.0),
                    "tier_weight_actual": float(r.tier_weight_actual or 0.0),
                },
                description=f"tier snapshot for {tier_name}",
            )
        )

    # Realisation proxy: weighted average actual weight coverage.
    if actual_weights:
        realisation = round(
            sum(actual_weights.values()) / len(actual_weights) * 100.0, 2
        )
    else:
        realisation = None

    applied = _filters_applied_from(filters)
    lineage = LineageBlock(
        formula=(
            "Pyramid tiers read from programme_rates for the latest snapshot "
            "in the window. Utilisation per tier averaged from resource_pool "
            "rows assigned to the programme. RAG = max |planned_weight - "
            "actual_weight| across tiers; green <=5pp, amber <=15pp, else red."
        ),
        formula_ref="PRD section 6.5 and FORMULAS.md entry 55",
        entries=lineage_entries,
        entries_total_count=len(lineage_entries),
        sampling="full",
    )

    return PyramidOut(
        programme_code=code,
        snapshot_date=latest_date,
        tiers=tiers_out,
        realisation_rate_pct=realisation,
        rag=_pyramid_rag(planned_weights, actual_weights),  # type: ignore[arg-type]
        filters_applied=applied,
        lineage=lineage,
    )


# --- endpoint 5: losses ------------------------------------------------


_LOSS_TARGET_GROSS_MARGIN = 0.30


@router.get(
    "/losses/{programme_code}",
    response_model=LossesOut,
    response_model_by_alias=True,
    summary="Seven delivery losses with revenue-foregone and margin-points-lost attribution",
)
async def losses(
    programme_code: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> LossesOut:
    """Return loss_exposure rows for a programme, plus attribution fields.

    ``revenue_foregone = loss_amount / (1 - target_margin)`` with target
    fixed at 30 percent gross per PRD 6.4. ``margin_points_lost_programme_bps
    = loss_amount / programme_revenue * 10000``. ``margin_points_lost_portfolio_bps
    = loss_amount / portfolio_revenue * 10000``. Programme revenue uses
    the latest Monthly Actuals row under the filters; portfolio revenue
    sums all programmes' latest Monthly Actuals.
    """
    code = programme_code.upper()
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    # Loss rows filtered by programme and date window.
    loss_stmt = select(LossExposure).where(LossExposure.program_id == programme.id)
    if filters.date_from is not None:
        loss_stmt = loss_stmt.where(LossExposure.snapshot_date >= filters.date_from)
    if filters.date_to is not None:
        loss_stmt = loss_stmt.where(LossExposure.snapshot_date <= filters.date_to)
    loss_stmt = loss_stmt.order_by(LossExposure.amount.desc())
    loss_rows = list((await session.execute(loss_stmt)).scalars().all())

    # Programme revenue: latest Monthly Actuals within the window.
    prog_row = await _latest_commercial_for(session, programme.id, filters)
    programme_revenue = float(prog_row.actual_revenue) if prog_row and prog_row.actual_revenue else 0.0

    # Portfolio revenue: sum across programmes' latest Monthly Actuals.
    all_programmes_stmt = select(Program)
    all_programmes = (await session.execute(all_programmes_stmt)).scalars().all()
    portfolio_revenue = 0.0
    for p in all_programmes:
        row = await _latest_commercial_for(session, p.id, filters)
        if row and row.actual_revenue:
            portfolio_revenue += float(row.actual_revenue)

    rows_out: list[LossRow] = []
    lineage_entries: list[LineageEntry] = []
    for r in loss_rows:
        amount = float(r.amount or 0.0)
        rev_foregone = round(amount / (1 - _LOSS_TARGET_GROSS_MARGIN), 0) if amount else 0.0
        prog_bps = round((amount / programme_revenue) * 10000, 2) if programme_revenue > 0 else 0.0
        port_bps = round((amount / portfolio_revenue) * 10000, 2) if portfolio_revenue > 0 else 0.0
        rows_out.append(
            LossRow(
                loss_category=r.loss_category,
                amount=amount,
                revenue_foregone=rev_foregone,
                margin_points_lost_programme_bps=prog_bps,
                margin_points_lost_portfolio_bps=port_bps,
                snapshot_date=r.snapshot_date,
                mitigation_status=r.mitigation_status,
            )
        )
        lineage_entries.append(
            LineageEntry(
                composite_key=f"{code}|{r.snapshot_date.isoformat() if r.snapshot_date else 'none'}|{r.loss_category}|loss_exposure",
                program_code=code,
                snapshot_date=r.snapshot_date,
                table="loss_exposure",
                row_id=r.id,
                columns_used={"loss_category": r.loss_category, "amount": amount},
                description="loss row feeding revenue-foregone and margin-points-lost",
            )
        )

    applied = _filters_applied_from(filters)
    lineage = LineageBlock(
        formula=(
            "revenue_foregone = amount / (1 - target_gross_margin_pct). "
            "margin_points_lost_programme_bps = amount / programme_revenue * 10000. "
            "margin_points_lost_portfolio_bps = amount / portfolio_revenue * 10000."
        ),
        formula_ref="PRD section 6.4 and FORMULAS.md entries 22-28",
        entries=lineage_entries,
        entries_total_count=len(lineage_entries),
        sampling="full",
    )
    return LossesOut(
        programme_code=code,
        target_gross_margin_pct=_LOSS_TARGET_GROSS_MARGIN,
        programme_revenue=programme_revenue,
        portfolio_revenue=portfolio_revenue,
        rows=rows_out,
        filters_applied=applied,
        lineage=lineage,
    )


# --- endpoint 6: evm ---------------------------------------------------


@router.get(
    "/evm/{programme_code}",
    response_model=EvmOut,
    response_model_by_alias=True,
    summary="Earned value metrics (CPI, SPI, EAC, TCPI, BAC, VAC) per programme",
)
async def evm(
    programme_code: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> EvmOut:
    """Return the latest EVM snapshot for a programme under active filters.

    Values come straight from ``evm_snapshots``. CPI and SPI are read as
    stored; EAC, TCPI, VAC are the seeded computed values from the EVM
    seed helper. Returns 200 with null values if no snapshot matches.
    """
    code = programme_code.upper()
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    stmt = select(EvmSnapshot).where(EvmSnapshot.program_id == programme.id)
    if filters.date_from is not None:
        stmt = stmt.where(EvmSnapshot.snapshot_date >= filters.date_from)
    if filters.date_to is not None:
        stmt = stmt.where(EvmSnapshot.snapshot_date <= filters.date_to)
    stmt = stmt.order_by(EvmSnapshot.snapshot_date.desc())
    row = (await session.execute(stmt)).scalars().first()

    applied = _filters_applied_from(filters)
    if row is None:
        return EvmOut(
            programme_code=code,
            snapshot_date=None,
            planned_value=None,
            earned_value=None,
            actual_cost=None,
            percent_complete=None,
            bac=None,
            cpi=None,
            spi=None,
            eac=None,
            tcpi=None,
            vac=None,
            filters_applied=applied,
            lineage=LineageBlock(
                formula="no evm_snapshots row under active filters",
                formula_ref="PRD section 6.3 and FORMULAS.md entries 7-13",
                entries=[],
                entries_total_count=0,
                sampling="full",
            ),
        )

    entry = LineageEntry(
        composite_key=f"{code}|{row.snapshot_date.isoformat()}|evm_snapshots",
        program_code=code,
        snapshot_date=row.snapshot_date,
        table="evm_snapshots",
        row_id=row.id,
        columns_used={
            "planned_value": float(row.planned_value) if row.planned_value is not None else None,
            "earned_value": float(row.earned_value) if row.earned_value is not None else None,
            "actual_cost": float(row.actual_cost) if row.actual_cost is not None else None,
            "cpi": float(row.cpi) if row.cpi is not None else None,
            "spi": float(row.spi) if row.spi is not None else None,
        },
        description="latest evm snapshot within window",
    )
    return EvmOut(
        programme_code=code,
        snapshot_date=row.snapshot_date,
        planned_value=float(row.planned_value) if row.planned_value is not None else None,
        earned_value=float(row.earned_value) if row.earned_value is not None else None,
        actual_cost=float(row.actual_cost) if row.actual_cost is not None else None,
        percent_complete=float(row.percent_complete) if row.percent_complete is not None else None,
        bac=float(row.bac) if row.bac is not None else None,
        cpi=float(row.cpi) if row.cpi is not None else None,
        spi=float(row.spi) if row.spi is not None else None,
        eac=float(row.eac) if row.eac is not None else None,
        tcpi=float(row.tcpi) if row.tcpi is not None else None,
        vac=float(row.vac) if row.vac is not None else None,
        filters_applied=applied,
        lineage=LineageBlock(
            formula=(
                "CPI = EV/AC. SPI = EV/PV. EAC = BAC/CPI. TCPI = (BAC-EV)/(BAC-AC). "
                "VAC = BAC-EAC. Values read from evm_snapshots."
            ),
            formula_ref="PRD section 6.3 and FORMULAS.md entries 7-13",
            entries=[entry],
            entries_total_count=1,
            sampling="full",
        ),
    )


# --- endpoint 7: dso ---------------------------------------------------


@router.get(
    "/dso/{programme_code}",
    response_model=DsoOut,
    response_model_by_alias=True,
    summary="Days Sales Outstanding, Unbilled WIP, AR balance per programme",
)
async def dso(
    programme_code: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> DsoOut:
    """DSO card backed by the M2 billing-column backfill.

    ``DSO_days = (ar_balance / billed_revenue) * 30`` per PRD 6.1 card 6
    and FORMULAS.md entry 54. Returns 200 with null values when no row
    matches so the frontend keeps a stable envelope shape.
    """
    code = programme_code.upper()
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    row = await _latest_commercial_for(session, programme.id, filters)
    applied = _filters_applied_from(filters)
    if row is None:
        return DsoOut(
            programme_code=code,
            snapshot_date=None,
            scenario_name=None,
            billed_revenue=None,
            collected_revenue=None,
            ar_balance=None,
            unbilled_wip=None,
            dso_days=None,
            filters_applied=applied,
            lineage=LineageBlock(
                formula="no commercial_scenarios row under active filters",
                formula_ref="PRD section 6.1 card 6 and FORMULAS.md entry 54",
                entries=[],
                entries_total_count=0,
                sampling="full",
            ),
        )

    billed = float(row.billed_revenue) if row.billed_revenue is not None else None
    collected = float(row.collected_revenue) if row.collected_revenue is not None else None
    ar = float(row.ar_balance) if row.ar_balance is not None else None
    unbilled = float(row.unbilled_wip) if row.unbilled_wip is not None else None
    dso_days = round((ar / billed) * 30, 2) if billed and ar is not None and billed > 0 else None

    entry = LineageEntry(
        composite_key=f"{code}|{row.snapshot_date.isoformat()}|{row.scenario_name}|commercial_scenarios",
        program_code=code,
        snapshot_date=row.snapshot_date,
        scenario_name=row.scenario_name,
        table="commercial_scenarios",
        row_id=row.id,
        columns_used={
            "billed_revenue": billed,
            "collected_revenue": collected,
            "ar_balance": ar,
            "unbilled_wip": unbilled,
        },
        description="billing and cash columns backfilled in M2",
    )
    return DsoOut(
        programme_code=code,
        snapshot_date=row.snapshot_date,
        scenario_name=row.scenario_name,
        billed_revenue=billed,
        collected_revenue=collected,
        ar_balance=ar,
        unbilled_wip=unbilled,
        dso_days=dso_days,
        filters_applied=applied,
        lineage=LineageBlock(
            formula=(
                "DSO_days = (ar_balance / billed_revenue) * 30. "
                "ar_balance = billed_revenue - collected_revenue. "
                "unbilled_wip = max(actual_revenue - billed_revenue, 0)."
            ),
            formula_ref="PRD section 6.1 card 6 and FORMULAS.md entry 54",
            entries=[entry],
            entries_total_count=1,
            sampling="full",
        ),
    )


# --- endpoint 8: revenue ------------------------------------------------


@router.get(
    "/revenue/{programme_code}",
    response_model=RevenueOut,
    response_model_by_alias=True,
    summary="Five revenue cards (Committed, Booked, Billed, Collected, Unbilled WIP)",
)
async def revenue(
    programme_code: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> RevenueOut:
    """Return the five revenue cards for a programme.

    Each card maps to a real commercial_scenarios column per M2 seed:

      committed_revenue   planned_revenue
      booked_revenue      actual_revenue
      billed_revenue      billed_revenue
      collected_revenue   collected_revenue
      unbilled_wip        unbilled_wip

    Values come from the latest Monthly Actuals row under the filters.
    No fabrication; if a column is null in the row the card reports null.
    """
    code = programme_code.upper()
    programme = await _lookup_programme(session, code)
    if programme is None:
        raise HTTPException(status_code=404, detail=f"programme '{code}' not found")

    row = await _latest_commercial_for(session, programme.id, filters)
    applied = _filters_applied_from(filters)

    if row is None:
        return RevenueOut(
            programme_code=code,
            snapshot_date=None,
            scenario_name=None,
            cards=[],
            filters_applied=applied,
            lineage=LineageBlock(
                formula="no commercial_scenarios row under active filters",
                formula_ref="PRD section 6.1 cards 1-5",
                entries=[],
                entries_total_count=0,
                sampling="full",
            ),
        )

    def _f(v: object) -> float | None:
        return float(v) if v is not None else None

    cards = [
        RevenueCard(
            card_key="committed_revenue", label="Committed revenue",
            value=_f(row.planned_revenue), source_column="planned_revenue",
        ),
        RevenueCard(
            card_key="booked_revenue", label="Booked revenue",
            value=_f(row.actual_revenue), source_column="actual_revenue",
        ),
        RevenueCard(
            card_key="billed_revenue", label="Billed revenue",
            value=_f(row.billed_revenue), source_column="billed_revenue",
        ),
        RevenueCard(
            card_key="collected_revenue", label="Collected revenue",
            value=_f(row.collected_revenue), source_column="collected_revenue",
        ),
        RevenueCard(
            card_key="unbilled_wip", label="Unbilled WIP",
            value=_f(row.unbilled_wip), source_column="unbilled_wip",
        ),
    ]
    entry = LineageEntry(
        composite_key=f"{code}|{row.snapshot_date.isoformat()}|{row.scenario_name}|commercial_scenarios",
        program_code=code,
        snapshot_date=row.snapshot_date,
        scenario_name=row.scenario_name,
        table="commercial_scenarios",
        row_id=row.id,
        columns_used={c.source_column: c.value for c in cards},
        description="five revenue cards read directly from commercial_scenarios",
    )
    return RevenueOut(
        programme_code=code,
        snapshot_date=row.snapshot_date,
        scenario_name=row.scenario_name,
        cards=cards,
        filters_applied=applied,
        lineage=LineageBlock(
            formula=(
                "Five revenue cards sourced from commercial_scenarios: "
                "Committed = planned_revenue. Booked = actual_revenue. "
                "Billed = billed_revenue. Collected = collected_revenue. "
                "Unbilled = unbilled_wip."
            ),
            formula_ref="PRD section 6.1 cards 1-5 (M3b v5.7.0 addition)",
            entries=[entry],
            entries_total_count=1,
            sampling="full",
        ),
    )


# --- endpoint 9: lineage ------------------------------------------------


async def _resolve_lineage(
    session: AsyncSession,
    parsed_key: str,
    tab: str,
    metric: str,
    slice_: str,
    aggregation: str,
    filters: PnlFilters,
) -> tuple[bool, str, str, float | None, str, list[LineageAtomicRow]]:
    """Return (supported, formula, formula_ref, value, unit, atomic_rows).

    Supported metric_key patterns in M3b (M9 will extend):

      pnl.gross_margin_pct.programme.month
      pnl.dso.programme.month
      pnl.cpi.programme.month
      pnl.spi.programme.month
      pnl.bench_cost.portfolio.current
    """
    programme_filter = filters.programmes[0] if filters.programmes else None

    # gross_margin_pct from commercial_scenarios
    if tab == "pnl" and metric == "gross_margin_pct" and slice_ == "programme":
        if not programme_filter:
            raise HTTPException(
                status_code=400,
                detail="lineage for slice=programme requires a 'programme' filter",
            )
        programme = await _lookup_programme(session, programme_filter)
        if programme is None:
            raise HTTPException(status_code=404, detail=f"programme '{programme_filter}' not found")
        row = await _latest_commercial_for(session, programme.id, filters)
        value = float(row.gross_margin_pct) if row and row.gross_margin_pct is not None else None
        atomic = (
            [
                LineageAtomicRow(
                    composite_key=f"{programme_filter}|{row.snapshot_date.isoformat()}|{row.scenario_name}|commercial_scenarios",
                    table="commercial_scenarios",
                    row_id=row.id,
                    program_code=programme_filter,
                    snapshot_date=row.snapshot_date,
                    scenario_name=row.scenario_name,
                    columns_used={
                        "actual_revenue": float(row.actual_revenue or 0.0),
                        "actual_cost": float(row.actual_cost or 0.0),
                        "gross_margin_pct": value,
                    },
                )
            ]
            if row
            else []
        )
        return (
            True,
            "(actual_revenue - actual_cost) / actual_revenue",
            "FORMULAS.md entry 14 Gross Margin Percentage",
            value,
            "ratio",
            atomic,
        )

    # dso from commercial_scenarios
    if tab == "pnl" and metric == "dso" and slice_ == "programme":
        if not programme_filter:
            raise HTTPException(
                status_code=400,
                detail="lineage for slice=programme requires a 'programme' filter",
            )
        programme = await _lookup_programme(session, programme_filter)
        if programme is None:
            raise HTTPException(status_code=404, detail=f"programme '{programme_filter}' not found")
        row = await _latest_commercial_for(session, programme.id, filters)
        value: float | None = None
        atomic_rows: list[LineageAtomicRow] = []
        if row and row.billed_revenue and row.billed_revenue > 0 and row.ar_balance is not None:
            value = round((float(row.ar_balance) / float(row.billed_revenue)) * 30, 2)
            atomic_rows = [
                LineageAtomicRow(
                    composite_key=f"{programme_filter}|{row.snapshot_date.isoformat()}|{row.scenario_name}|commercial_scenarios",
                    table="commercial_scenarios",
                    row_id=row.id,
                    program_code=programme_filter,
                    snapshot_date=row.snapshot_date,
                    scenario_name=row.scenario_name,
                    columns_used={
                        "billed_revenue": float(row.billed_revenue),
                        "ar_balance": float(row.ar_balance),
                    },
                )
            ]
        return (
            True,
            "(ar_balance / billed_revenue) * 30",
            "FORMULAS.md entry 54 DSO and AR balance",
            value,
            "days",
            atomic_rows,
        )

    # cpi and spi from evm_snapshots
    if tab == "pnl" and metric in {"cpi", "spi"} and slice_ == "programme":
        if not programme_filter:
            raise HTTPException(
                status_code=400,
                detail="lineage for slice=programme requires a 'programme' filter",
            )
        programme = await _lookup_programme(session, programme_filter)
        if programme is None:
            raise HTTPException(status_code=404, detail=f"programme '{programme_filter}' not found")
        stmt = (
            select(EvmSnapshot)
            .where(EvmSnapshot.program_id == programme.id)
            .order_by(EvmSnapshot.snapshot_date.desc())
        )
        row = (await session.execute(stmt)).scalars().first()
        value = float(getattr(row, metric)) if row and getattr(row, metric) is not None else None
        atomic_rows = (
            [
                LineageAtomicRow(
                    composite_key=f"{programme_filter}|{row.snapshot_date.isoformat()}|evm_snapshots",
                    table="evm_snapshots",
                    row_id=row.id,
                    program_code=programme_filter,
                    snapshot_date=row.snapshot_date,
                    scenario_name=None,
                    columns_used={metric: value},
                )
            ]
            if row
            else []
        )
        formula = "EV / AC" if metric == "cpi" else "EV / PV"
        ref = (
            "FORMULAS.md entry 7 Cost Performance Index"
            if metric == "cpi"
            else "FORMULAS.md entry 13 Schedule Performance Index"
        )
        return True, formula, ref, value, "ratio", atomic_rows

    # Unsupported: return not-supported placeholder. This is M9 fodder.
    return (
        False,
        "resolver not implemented for this metric_key",
        None,  # type: ignore[return-value]
        None,
        "none",
        [],
    )


@router.get(
    "/lineage/{metric_key}",
    response_model=LineageResolverOut,
    response_model_by_alias=True,
    summary="Atomic row set, formula reference, and value for a single metric key",
)
async def lineage_resolve(
    metric_key: str,
    filters: PnlFilters = Depends(pnl_filters_dependency),
    session: AsyncSession = Depends(get_session),
) -> LineageResolverOut:
    """Resolve a lineage key to the atomic rows that produced its value.

    Supported keys in M3b (M9 extends the resolver to all 12 tabs):

      pnl.gross_margin_pct.programme.month
      pnl.dso.programme.month
      pnl.cpi.programme.month
      pnl.spi.programme.month

    Unsupported keys return 200 with ``supported=false`` and an empty
    ``atomic_rows`` list so callers distinguish a miss from a parse error.
    Malformed keys still raise LineageKeyError (422) via the parser.
    """
    parsed = parse_lineage_key(metric_key)
    supported, formula, formula_ref, value, unit, atomic = await _resolve_lineage(
        session,
        metric_key,
        parsed.tab,
        parsed.metric,
        parsed.slice,
        parsed.aggregation,
        filters,
    )

    applied = _filters_applied_from(filters)
    lineage_entries = [
        LineageEntry(
            composite_key=a.composite_key,
            program_code=a.program_code,
            snapshot_date=a.snapshot_date,
            scenario_name=a.scenario_name,
            table=a.table,
            row_id=a.row_id,
            columns_used=a.columns_used,
            description="contributing row",
        )
        for a in atomic
    ]
    return LineageResolverOut(
        metric_key=metric_key,
        parsed=parsed.as_dict(),
        supported=supported,
        formula=formula,
        formula_ref=formula_ref,
        value=value,
        unit=unit,
        atomic_rows=atomic,
        filters_applied=applied,
        lineage=LineageBlock(
            formula=formula,
            formula_ref=formula_ref,
            entries=lineage_entries,
            entries_total_count=len(lineage_entries),
            sampling="full",
        ),
    )
