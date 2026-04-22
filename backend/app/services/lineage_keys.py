"""Lineage key parser and validator for v5.7.0 Tab 12 and M9 drill support.

A lineage key is a four-segment dotted string that names a metric cell
precisely enough for the backend to resolve it to contributing atomic rows.
The format is locked per session decision on 2026-04-22 and documented in
``docs/LINEAGE_KEYS.md``.

Pattern: ``{tab}.{metric}.{slice}.{aggregation}``

Rules:

- Lowercase ASCII only. Underscores allowed inside a segment; dots separate
  segments. Exactly four segments.
- ``tab`` belongs to a fixed vocabulary. ``slice`` and ``aggregation`` each
  belong to fixed vocabularies too. ``metric`` is looser because it names a
  formula identifier that may be added over time.
- If a dimension does not apply, use the literal ``none`` in that slot. No
  empty segments.

Examples:

    pnl.gross_margin_pct.programme.month
    executive.utilisation.resource.current
    delivery.cpi.programme.rolling_3m
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

# Fixed vocabularies. Add new entries here and in docs/LINEAGE_KEYS.md at
# the same time. Never remove entries without a two-version deprecation
# window recorded in the docs, per the translation-table rule.
_TABS: Final[frozenset[str]] = frozenset(
    {
        "pnl",
        "executive",
        "delivery",
        "risk",
        "flow",
        "financials",
        "ai",
        "bench",
        "commercial",
        "backlog",
        "scenario",
        "ops",
    }
)
_SLICES: Final[frozenset[str]] = frozenset(
    {"programme", "resource", "sprint", "month", "phase", "portfolio", "none"}
)
_AGGREGATIONS: Final[frozenset[str]] = frozenset(
    {"current", "month", "quarter", "ytd", "rolling_3m", "none"}
)

# Segment pattern. Lowercase letters, digits, and underscores. At least one
# character. No leading or trailing underscores to keep the format tidy.
_SEGMENT_RE: Final[re.Pattern[str]] = re.compile(r"^[a-z][a-z0-9_]*[a-z0-9]$|^[a-z0-9]$")


class LineageKeyError(ValueError):
    """Raised when a lineage key fails validation.

    Carries the offending key and a plain-language reason. FastAPI error
    handlers translate this to a 422 response with the standard error
    envelope.
    """

    def __init__(self, key: str, reason: str) -> None:
        self.key = key
        self.reason = reason
        super().__init__(f"invalid lineage key '{key}': {reason}")


@dataclass(frozen=True, slots=True)
class LineageKey:
    """Parsed lineage key. Immutable once constructed."""

    raw: str
    tab: str
    metric: str
    slice: str
    aggregation: str

    def as_dict(self) -> dict[str, str]:
        return {
            "raw": self.raw,
            "tab": self.tab,
            "metric": self.metric,
            "slice": self.slice,
            "aggregation": self.aggregation,
        }


def parse(key: str) -> LineageKey:
    """Parse and validate a lineage key.

    Raises ``LineageKeyError`` if the key is malformed.
    """
    if key is None:
        raise LineageKeyError(str(key), "key is required")
    if not isinstance(key, str):
        raise LineageKeyError(str(key), "key must be a string")
    if not key:
        raise LineageKeyError(key, "key is empty")

    segments = key.split(".")
    if len(segments) != 4:
        raise LineageKeyError(
            key,
            f"expected 4 dot-separated segments, got {len(segments)}",
        )

    tab, metric, slice_, aggregation = segments

    # Per-segment character check, catches uppercase, hyphens, unicode, etc.
    for label, value in (
        ("tab", tab),
        ("metric", metric),
        ("slice", slice_),
        ("aggregation", aggregation),
    ):
        if not value:
            raise LineageKeyError(key, f"{label} segment is empty")
        if not _SEGMENT_RE.fullmatch(value):
            raise LineageKeyError(
                key,
                f"{label} segment '{value}' must be lowercase ASCII with underscores",
            )

    if tab not in _TABS:
        raise LineageKeyError(
            key,
            f"unknown tab '{tab}'; allowed: {sorted(_TABS)}",
        )
    if slice_ not in _SLICES:
        raise LineageKeyError(
            key,
            f"unknown slice '{slice_}'; allowed: {sorted(_SLICES)}",
        )
    if aggregation not in _AGGREGATIONS:
        raise LineageKeyError(
            key,
            f"unknown aggregation '{aggregation}'; allowed: {sorted(_AGGREGATIONS)}",
        )

    return LineageKey(
        raw=key,
        tab=tab,
        metric=metric,
        slice=slice_,
        aggregation=aggregation,
    )


def is_valid(key: str) -> bool:
    """Return True if ``key`` parses cleanly, False otherwise."""
    try:
        parse(key)
    except LineageKeyError:
        return False
    return True


# Public re-exports for modules that prefer reading vocabularies directly.
TABS: Final[frozenset[str]] = _TABS
SLICES: Final[frozenset[str]] = _SLICES
AGGREGATIONS: Final[frozenset[str]] = _AGGREGATIONS
