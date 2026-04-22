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
