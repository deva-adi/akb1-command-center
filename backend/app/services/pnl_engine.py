"""Pure functions for v5.7.0 Tab 12 P&L computations.

Kept I/O free so every function is trivially unit-testable and every
endpoint can rely on deterministic output for a fixed seed. No FastAPI
imports, no database imports, no clock access.

Two primary computations land here in M3b first wave:

  compute_waterfall
      Reads a commercial_scenarios row and returns the four-layer margin
      breakdown (Gross, Contribution, Portfolio, Net) used by the
      /api/v1/pnl/waterfall endpoint.

  compute_bridge
      Reads a prior and a current commercial_scenarios row (plus the
      matching programme_rates tier snapshots) and returns the
      Price/Volume/Mix/Cost decomposition used by the /api/v1/pnl/bridge
      endpoint. Cost is the residual by construction so the four
      drivers always sum to the total delta exactly.

Remaining endpoints (pfa, pyramid, losses, evm, dso, revenue, lineage)
plug into helpers added in M3b second wave.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class CommercialSnapshot:
    """Inputs for a single commercial_scenarios row used by the engine."""

    actual_revenue: float
    actual_cost: float
    gross_margin_pct: float
    contribution_margin_pct: float | None
    portfolio_margin_pct: float | None
    net_margin_pct: float | None


@dataclass(frozen=True, slots=True)
class WaterfallLayer:
    """One rung of the four-layer margin waterfall."""

    layer: Literal["gross", "contribution", "portfolio", "net"]
    label: str
    margin_pct: float | None
    margin_value: float | None


@dataclass(frozen=True, slots=True)
class WaterfallBreakdown:
    """Output of compute_waterfall."""

    revenue: float
    layers: list[WaterfallLayer]


def compute_waterfall(row: CommercialSnapshot) -> WaterfallBreakdown:
    """Return the four margin layers from one commercial_scenarios row.

    ``margin_value`` is ``margin_pct * actual_revenue`` so the waterfall
    can render as dollar bars. Layers with a null pct in the seed return
    null ``margin_pct`` and null ``margin_value`` so the client can
    render a placeholder rather than a fake number.
    """
    revenue = float(row.actual_revenue)

    def _layer(layer_name: Literal["gross", "contribution", "portfolio", "net"], label: str, pct: float | None) -> WaterfallLayer:
        if pct is None:
            return WaterfallLayer(layer=layer_name, label=label, margin_pct=None, margin_value=None)
        return WaterfallLayer(
            layer=layer_name,
            label=label,
            margin_pct=float(pct),
            margin_value=round(float(pct) * revenue, 2),
        )

    return WaterfallBreakdown(
        revenue=revenue,
        layers=[
            _layer("gross", "Gross margin", row.gross_margin_pct),
            _layer("contribution", "Contribution margin", row.contribution_margin_pct),
            _layer("portfolio", "Portfolio margin", row.portfolio_margin_pct),
            _layer("net", "Net margin", row.net_margin_pct),
        ],
    )


@dataclass(frozen=True, slots=True)
class TierSnapshot:
    """One programme_rates row used by the bridge decomposition."""

    role_tier: str
    planned_rate: float
    actual_rate: float
    tier_weight_planned: float
    tier_weight_actual: float


@dataclass(frozen=True, slots=True)
class BridgeDrivers:
    """Four driver buckets. Cost is the residual so the total always ties."""

    price_bps: float
    volume_bps: float
    mix_bps: float
    cost_bps_residual: float

    @property
    def total_bps(self) -> float:
        return self.price_bps + self.volume_bps + self.mix_bps + self.cost_bps_residual


@dataclass(frozen=True, slots=True)
class BridgeBreakdown:
    """Output of compute_bridge."""

    prior_value: float
    current_value: float
    total_delta_bps: float
    drivers: BridgeDrivers


def _blended_rate(tiers: list[TierSnapshot]) -> float:
    """Weight-averaged actual rate across tiers.

    Uses ``tier_weight_actual`` as the weighting. Returns 0 if weights
    sum to zero so callers can guard against divide-by-zero.
    """
    total_weight = sum(t.tier_weight_actual for t in tiers)
    if total_weight <= 0:
        return 0.0
    return sum(t.actual_rate * t.tier_weight_actual for t in tiers) / total_weight


def compute_bridge(
    prior: CommercialSnapshot,
    current: CommercialSnapshot,
    tiers_prior: list[TierSnapshot],
    tiers_current: list[TierSnapshot],
) -> BridgeBreakdown:
    """Decompose the gross-margin delta between two snapshots.

    Definitions locked with Adi during M3b mid-checkpoint rework
    (2026-04-22). The decomposition operates on per-tier implied hours
    derived from ``actual_revenue / blended_rate`` so the maths stays
    grounded in the seed numbers without needing a hours table.

    Price per tier
        ``(current_rate - base_rate) * base_hours``.
        Weight held constant at the base period. Captures pure intra-tier
        rate drift only.

    Volume total
        ``(current_total_hours - base_total_hours) * base_blended_rate``.
        Captures the hours-compression contribution at the base blended
        rate, so no Price leakage into Volume.

    Mix per tier
        ``current_rate * (current_hours - base_hours * current_total / base_total)``.
        Rate held at the current period. The inner term is the tier hours
        minus what the tier would have held if the base distribution
        rescaled proportionally to the current total. Captures the weight
        shift only.

    Cost residual
        ``total_delta_bps - (Price_bps + Volume_bps + Mix_bps)``.
        Absorbs cost pressure, second-order interactions, and any
        modelling imprecision in the other three drivers. This is the
        accounting-closure term that guarantees the four drivers sum to
        total_delta_bps exactly for every input.

    Each dollar-denominated effect is scaled to basis points as
    ``bps = (dollars / base_revenue) * 10000``. ``total_delta_bps`` is
    computed directly from ``gross_margin_pct`` so the value reconciles
    to the seed (M2 reconciliation gate: Phoenix Feb-to-Mar = -340 bps).
    """
    total_delta_bps = round((current.gross_margin_pct - prior.gross_margin_pct) * 10000, 2)
    base_revenue = float(prior.actual_revenue)

    # Nothing to decompose if we cannot form implied hours.
    if base_revenue <= 0:
        return BridgeBreakdown(
            prior_value=float(prior.gross_margin_pct),
            current_value=float(current.gross_margin_pct),
            total_delta_bps=total_delta_bps,
            drivers=BridgeDrivers(
                price_bps=0.0,
                volume_bps=0.0,
                mix_bps=0.0,
                cost_bps_residual=total_delta_bps,
            ),
        )

    base_blended = _blended_rate(tiers_prior)
    current_blended = _blended_rate(tiers_current)

    # Without blended rates we cannot form implied hours; Cost absorbs
    # the full delta.
    if base_blended <= 0 or current_blended <= 0 or not tiers_prior or not tiers_current:
        return BridgeBreakdown(
            prior_value=float(prior.gross_margin_pct),
            current_value=float(current.gross_margin_pct),
            total_delta_bps=total_delta_bps,
            drivers=BridgeDrivers(
                price_bps=0.0,
                volume_bps=0.0,
                mix_bps=0.0,
                cost_bps_residual=total_delta_bps,
            ),
        )

    # --- Implied hours -----------------------------------------------------
    # Revenue = blended_rate * total_hours, so total_hours = revenue / blended.
    # Per-tier hours follow tier_weight_actual of that total.
    base_total_hours = base_revenue / base_blended
    current_total_hours = float(current.actual_revenue) / current_blended

    base_hours_by_tier = {
        t.role_tier: t.tier_weight_actual * base_total_hours for t in tiers_prior
    }
    current_hours_by_tier = {
        t.role_tier: t.tier_weight_actual * current_total_hours for t in tiers_current
    }
    base_rate_by_tier = {t.role_tier: t.actual_rate for t in tiers_prior}
    current_rate_by_tier = {t.role_tier: t.actual_rate for t in tiers_current}

    tier_keys = set(base_hours_by_tier) & set(current_hours_by_tier)

    # --- Price effect (dollars) -------------------------------------------
    price_dollars = 0.0
    for tier in tier_keys:
        base_rate = base_rate_by_tier[tier]
        current_rate = current_rate_by_tier[tier]
        base_hours = base_hours_by_tier[tier]
        price_dollars += (current_rate - base_rate) * base_hours

    # --- Volume effect (dollars) ------------------------------------------
    volume_dollars = (current_total_hours - base_total_hours) * base_blended

    # --- Mix effect (dollars) ---------------------------------------------
    # current_rate * (current_hours - base_hours * current_total / base_total).
    # The inner term is "actual current hours minus proportionally-scaled
    # base hours at the current total". Zero if weights did not shift.
    scale = current_total_hours / base_total_hours if base_total_hours > 0 else 0.0
    mix_dollars = 0.0
    for tier in tier_keys:
        current_rate = current_rate_by_tier[tier]
        current_hours = current_hours_by_tier[tier]
        base_hours = base_hours_by_tier[tier]
        mix_dollars += current_rate * (current_hours - base_hours * scale)

    # --- Scale to bps on base revenue --------------------------------------
    price_bps = round((price_dollars / base_revenue) * 10000, 2)
    volume_bps = round((volume_dollars / base_revenue) * 10000, 2)
    mix_bps = round((mix_dollars / base_revenue) * 10000, 2)

    # --- Cost residual: closes the decomposition exactly ------------------
    cost_bps_residual = round(total_delta_bps - (price_bps + volume_bps + mix_bps), 2)

    return BridgeBreakdown(
        prior_value=float(prior.gross_margin_pct),
        current_value=float(current.gross_margin_pct),
        total_delta_bps=total_delta_bps,
        drivers=BridgeDrivers(
            price_bps=price_bps,
            volume_bps=volume_bps,
            mix_bps=mix_bps,
            cost_bps_residual=cost_bps_residual,
        ),
    )
