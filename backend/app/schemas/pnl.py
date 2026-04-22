"""Pydantic schemas shared across v5.7.0 Tab 12 P&L endpoints.

Three building blocks every endpoint composes:

- ``FiltersApplied``: echo of the resolved filter set. Breadcrumbs render
  from this block without re-parsing the request URL.
- ``LineageBlock``: formula expression plus the atomic row IDs that
  contributed to the response. Supports calculation-to-data drill in M9.
- ``ErrorEnvelope``: single shape every endpoint returns on error.

Per-endpoint response models live alongside this file as they ship in
M3b. This module defines only the shared shapes.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class FiltersApplied(BaseModel):
    """Canonical echo of the resolved filter set."""

    model_config = ConfigDict(extra="forbid")

    programme: list[str] | None = Field(default=None, description="Resolved programme codes")
    from_: date | None = Field(default=None, alias="from", description="Inclusive lower bound")
    to: date | None = Field(default=None, description="Inclusive upper bound")
    tier: Literal["Junior", "Mid", "Senior"] | None = Field(default=None)
    scenario_name: str | None = Field(default=None)
    portfolio: str | None = Field(default=None)
    month: date | None = Field(default=None)


class LineageEntry(BaseModel):
    """One contributing atomic row or formula input."""

    model_config = ConfigDict(extra="forbid")

    composite_key: str = Field(
        description="Human-readable identifier in the form <program>|<date>|<scenario>|<table>"
    )
    program_code: str | None = Field(default=None)
    snapshot_date: date | None = Field(default=None)
    scenario_name: str | None = Field(default=None)
    table: str | None = Field(default=None, description="Source table name")
    row_id: int | None = Field(default=None, description="Primary key of the source row")
    columns_used: dict[str, Any] | None = Field(
        default=None, description="Column values this row contributed"
    )
    description: str | None = Field(default=None, description="Plain-language role this row played")


class LineageBlock(BaseModel):
    """Formula expression plus atomic contributing rows.

    Every response wraps one. For large aggregations switch ``sampling``
    to ``"sampled"`` and include ``sampling_rule`` so callers can tell the
    difference.
    """

    model_config = ConfigDict(extra="forbid")

    formula: str = Field(description="SQL-equivalent or formula expression")
    formula_ref: str | None = Field(
        default=None, description="Reference to FORMULAS.md entry or PRD section"
    )
    entries: list[LineageEntry] = Field(default_factory=list)
    entries_total_count: int = Field(description="Total count before any sampling")
    sampling: Literal["full", "sampled"] = Field(default="full")
    sampling_rule: str | None = Field(
        default=None,
        description="Describes the sampling strategy when sampling=='sampled'",
    )


class ErrorEnvelopeBody(BaseModel):
    """Inner error payload."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(description="Stable machine-readable error code")
    message: str = Field(description="Human-readable message")
    details: dict[str, Any] | None = Field(default=None)


class ErrorEnvelope(BaseModel):
    """Standard error response shape.

    Every endpoint in v5.7.0 returns this on any non-2xx status. The
    ``filters_applied`` block is populated whenever the request got far
    enough to resolve filters, so frontend breadcrumbs still render.
    """

    model_config = ConfigDict(extra="forbid")

    error: ErrorEnvelopeBody
    filters_applied: FiltersApplied | None = Field(default=None)


class Pagination(BaseModel):
    """Pagination metadata included on list-shaped responses."""

    model_config = ConfigDict(extra="forbid")

    limit: int = Field(description="Maximum items requested")
    offset: int = Field(description="Zero-based offset applied")
    total: int = Field(description="Total items available under the current filters")
    returned: int = Field(description="Items returned in this response")


# --- Endpoint response models (M3b first wave: waterfall, bridge) -------


class WaterfallLayerOut(BaseModel):
    """One rung of the four-layer margin waterfall."""

    model_config = ConfigDict(extra="forbid")

    layer: Literal["gross", "contribution", "portfolio", "net"]
    label: str
    margin_pct: float | None = None
    margin_value: float | None = None


class WaterfallOut(BaseModel):
    """Response shape for GET /api/v1/pnl/waterfall/{programme_code}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    programme_code: str
    snapshot_date: date
    scenario_name: str
    revenue: float
    layers: list[WaterfallLayerOut]
    filters_applied: FiltersApplied
    lineage: LineageBlock


class BridgeDriversOut(BaseModel):
    """Price/Volume/Mix/Cost decomposition buckets."""

    model_config = ConfigDict(extra="forbid")

    price_bps: float
    volume_bps: float
    mix_bps: float
    cost_bps_residual: float


class BridgeOut(BaseModel):
    """Response shape for GET /api/v1/pnl/bridge/{metric_key}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    metric_key: str
    programme_code: str
    prior_snapshot_date: date
    current_snapshot_date: date
    prior_value: float
    current_value: float
    total_delta_bps: float
    drivers: BridgeDriversOut
    filters_applied: FiltersApplied
    lineage: LineageBlock


# --- /pfa --------------------------------------------------------------


class PfaPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    snapshot_date: date
    value: float | None


class PfaSeries(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan: list[PfaPoint]
    forecast: list[PfaPoint]
    actual: list[PfaPoint]


class PfaOut(BaseModel):
    """Response shape for GET /api/v1/pnl/pfa/{programme_code}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    programme_code: str
    metric: Literal["revenue", "gross_pct", "net_pct", "cpi", "spi"]
    series: PfaSeries
    filters_applied: FiltersApplied
    lineage: LineageBlock


# --- /pyramid ----------------------------------------------------------


class PyramidTier(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role_tier: Literal["Junior", "Mid", "Senior"]
    planned_headcount: int | None
    actual_headcount: int | None
    planned_weight: float | None
    actual_weight: float | None
    planned_rate: float | None
    actual_rate: float | None
    utilisation_pct: float | None


class PyramidOut(BaseModel):
    """Response shape for GET /api/v1/pnl/pyramid/{programme_code}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    programme_code: str
    snapshot_date: date | None
    tiers: list[PyramidTier]
    realisation_rate_pct: float | None
    rag: Literal["green", "amber", "red"]
    filters_applied: FiltersApplied
    lineage: LineageBlock


# --- /losses -----------------------------------------------------------


class LossRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    loss_category: str
    amount: float
    revenue_foregone: float
    margin_points_lost_programme_bps: float
    margin_points_lost_portfolio_bps: float
    snapshot_date: date | None
    mitigation_status: str | None


class LossesOut(BaseModel):
    """Response shape for GET /api/v1/pnl/losses/{programme_code}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    programme_code: str
    target_gross_margin_pct: float = Field(
        description="Denominator used for revenue-foregone calculation per PRD 6.4"
    )
    programme_revenue: float
    portfolio_revenue: float
    rows: list[LossRow]
    filters_applied: FiltersApplied
    lineage: LineageBlock


# --- /evm --------------------------------------------------------------


class EvmOut(BaseModel):
    """Response shape for GET /api/v1/pnl/evm/{programme_code}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    programme_code: str
    snapshot_date: date | None
    planned_value: float | None
    earned_value: float | None
    actual_cost: float | None
    percent_complete: float | None
    bac: float | None
    cpi: float | None
    spi: float | None
    eac: float | None
    tcpi: float | None
    vac: float | None
    filters_applied: FiltersApplied
    lineage: LineageBlock


# --- /dso --------------------------------------------------------------


class DsoOut(BaseModel):
    """Response shape for GET /api/v1/pnl/dso/{programme_code}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    programme_code: str
    snapshot_date: date | None
    scenario_name: str | None
    billed_revenue: float | None
    collected_revenue: float | None
    ar_balance: float | None
    unbilled_wip: float | None
    dso_days: float | None
    filters_applied: FiltersApplied
    lineage: LineageBlock


# --- /revenue ----------------------------------------------------------


class RevenueCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    card_key: Literal[
        "committed_revenue",
        "booked_revenue",
        "billed_revenue",
        "collected_revenue",
        "unbilled_wip",
    ]
    label: str
    value: float | None
    source_column: str


class RevenueOut(BaseModel):
    """Response shape for GET /api/v1/pnl/revenue/{programme_code}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    programme_code: str
    snapshot_date: date | None
    scenario_name: str | None
    cards: list[RevenueCard]
    filters_applied: FiltersApplied
    lineage: LineageBlock


# --- /lineage ----------------------------------------------------------


class LineageAtomicRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    composite_key: str
    table: str
    row_id: int | None
    program_code: str | None
    snapshot_date: date | None
    scenario_name: str | None
    columns_used: dict[str, Any] | None


class LineageResolverOut(BaseModel):
    """Response shape for GET /api/v1/pnl/lineage/{metric_key}."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    metric_key: str
    parsed: dict[str, str]
    supported: bool
    formula: str
    formula_ref: str | None
    value: float | None
    unit: str
    atomic_rows: list[LineageAtomicRow]
    filters_applied: FiltersApplied
    lineage: LineageBlock
