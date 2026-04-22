"""Universal query-filter parsing for v5.7.0 Tab 12 endpoints.

Canonical query parameter names:

    programme       comma-separated list of programme codes
    from            inclusive lower bound, YYYY-MM-DD
    to              inclusive upper bound, YYYY-MM-DD
    tier            Junior | Mid | Senior (short forms Jr, Sr also accepted)
    scenario_name   free text, length-capped
    portfolio       optional cohort label
    month           single month anchor, YYYY-MM-DD

Backwards-compat aliases. Older snippets and v5.6-era fixtures may still
use ``programme_code``, ``period_start``, ``period_end``. The parser
silently accepts these as aliases for ``programme``, ``from``, ``to``.
Response envelopes always emit the canonical form, never the alias.

Filters compose by AND. Absent filter means no constraint on that
dimension. Bad values raise ``FilterValidationError``, which the
standard error envelope handler turns into a 422 response.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Final, Literal

from fastapi import Query, Request

_VALID_TIERS_OUT: Final[frozenset[str]] = frozenset({"Junior", "Mid", "Senior"})
_TIER_ALIASES: Final[dict[str, str]] = {
    "jr": "Junior",
    "junior": "Junior",
    "mid": "Mid",
    "sr": "Senior",
    "senior": "Senior",
}
_MAX_SCENARIO_NAME_LEN: Final[int] = 100
_MAX_PORTFOLIO_LEN: Final[int] = 100
_MAX_PROGRAMME_CODES: Final[int] = 50


class FilterValidationError(ValueError):
    """Raised when a query filter has a bad value.

    The error envelope handler catches this and emits a 422 with a
    structured payload that echoes ``filters_applied`` so the frontend
    keeps breadcrumb context even on validation failure.
    """

    def __init__(self, field: str, reason: str, *, value: object | None = None) -> None:
        self.field = field
        self.reason = reason
        self.value = value
        super().__init__(f"invalid value for '{field}': {reason}")


@dataclass(frozen=True, slots=True)
class PnlFilters:
    """Canonical resolved filter set. Immutable."""

    programmes: tuple[str, ...] | None
    date_from: date | None
    date_to: date | None
    tier: Literal["Junior", "Mid", "Senior"] | None
    scenario_name: str | None
    portfolio: str | None
    month: date | None

    def to_applied_block(self) -> dict[str, object]:
        """Return the ``filters_applied`` dict every response echoes.

        Emits canonical field names only. Aliases never appear on the
        response side.
        """
        return {
            "programme": list(self.programmes) if self.programmes else None,
            "from": self.date_from.isoformat() if self.date_from else None,
            "to": self.date_to.isoformat() if self.date_to else None,
            "tier": self.tier,
            "scenario_name": self.scenario_name,
            "portfolio": self.portfolio,
            "month": self.month.isoformat() if self.month else None,
        }


def _parse_programme_list(raw: str | None) -> tuple[str, ...] | None:
    if raw is None or raw == "":
        return None
    codes = tuple(token.strip().upper() for token in raw.split(",") if token.strip())
    if not codes:
        return None
    if len(codes) > _MAX_PROGRAMME_CODES:
        raise FilterValidationError(
            "programme",
            f"up to {_MAX_PROGRAMME_CODES} programme codes allowed, got {len(codes)}",
            value=raw,
        )
    for code in codes:
        if not code.replace("-", "").replace("_", "").isalnum():
            raise FilterValidationError(
                "programme",
                f"programme code '{code}' must be alphanumeric with hyphens or underscores",
                value=raw,
            )
        if len(code) > 50:
            raise FilterValidationError(
                "programme",
                f"programme code '{code}' exceeds 50 characters",
                value=raw,
            )
    return codes


def _parse_iso_date(raw: str | None, field: str) -> date | None:
    if raw is None or raw == "":
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError as e:
        raise FilterValidationError(field, f"expected YYYY-MM-DD, got '{raw}'", value=raw) from e


def _parse_tier(raw: str | None) -> Literal["Junior", "Mid", "Senior"] | None:
    if raw is None or raw == "":
        return None
    normalised = _TIER_ALIASES.get(raw.lower())
    if normalised is None:
        raise FilterValidationError(
            "tier",
            f"expected Junior/Mid/Senior (or Jr/Sr), got '{raw}'",
            value=raw,
        )
    return normalised  # type: ignore[return-value]


def _parse_text(raw: str | None, field: str, max_len: int) -> str | None:
    if raw is None or raw == "":
        return None
    if len(raw) > max_len:
        raise FilterValidationError(
            field,
            f"value exceeds {max_len} characters",
            value=raw,
        )
    return raw


def _first_present(*values: str | None) -> str | None:
    """Return the first non-empty value, or None if all are empty.

    Used to pick between the canonical query param and an alias without
    preferring one over the other when both are present.
    """
    for v in values:
        if v is not None and v != "":
            return v
    return None


async def pnl_filters_dependency(
    request: Request,
    programme: str | None = Query(default=None, description="Comma-separated programme codes"),
    from_: str | None = Query(default=None, alias="from", description="Inclusive lower bound, YYYY-MM-DD"),
    to: str | None = Query(default=None, description="Inclusive upper bound, YYYY-MM-DD"),
    tier: str | None = Query(default=None, description="Junior, Mid, or Senior (Jr and Sr also accepted)"),
    scenario_name: str | None = Query(default=None, description="Scenario name filter"),
    portfolio: str | None = Query(default=None, description="Portfolio cohort label"),
    month: str | None = Query(default=None, description="Single-month anchor, YYYY-MM-DD"),
) -> PnlFilters:
    """FastAPI dependency that parses and validates universal PnL filters.

    Silently accepts these aliases for backwards compatibility with v5.6
    era snippets:

        programme_code  -> programme
        period_start    -> from
        period_end      -> to

    When both canonical and alias are present, the canonical wins. Bad
    values raise ``FilterValidationError`` which the app-level error
    handler converts to 422.
    """
    # Read the alias forms directly from query params since FastAPI cannot
    # bind ``period_start`` and ``from`` to the same parameter.
    query = request.query_params
    programme_raw = _first_present(programme, query.get("programme_code"))
    from_raw = _first_present(from_, query.get("period_start"))
    to_raw = _first_present(to, query.get("period_end"))

    return PnlFilters(
        programmes=_parse_programme_list(programme_raw),
        date_from=_parse_iso_date(from_raw, "from"),
        date_to=_parse_iso_date(to_raw, "to"),
        tier=_parse_tier(tier),
        scenario_name=_parse_text(scenario_name, "scenario_name", _MAX_SCENARIO_NAME_LEN),
        portfolio=_parse_text(portfolio, "portfolio", _MAX_PORTFOLIO_LEN),
        month=_parse_iso_date(month, "month"),
    )
