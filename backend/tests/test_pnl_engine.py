"""Pure-function tests for the M3b P&L engine (no DB, no FastAPI)."""
from __future__ import annotations

from app.services.pnl_engine import (
    CommercialSnapshot,
    TierSnapshot,
    compute_bridge,
    compute_waterfall,
)


class TestComputeWaterfall:
    def test_returns_four_layers_in_fixed_order(self) -> None:
        row = CommercialSnapshot(
            actual_revenue=820_000,
            actual_cost=590_000,
            gross_margin_pct=0.28,
            contribution_margin_pct=0.125,
            portfolio_margin_pct=0.082,
            net_margin_pct=0.041,
        )
        w = compute_waterfall(row)
        assert [layer.layer for layer in w.layers] == ["gross", "contribution", "portfolio", "net"]

    def test_margin_value_equals_pct_times_revenue(self) -> None:
        row = CommercialSnapshot(
            actual_revenue=1_000_000,
            actual_cost=800_000,
            gross_margin_pct=0.20,
            contribution_margin_pct=0.10,
            portfolio_margin_pct=0.05,
            net_margin_pct=0.02,
        )
        w = compute_waterfall(row)
        assert w.layers[0].margin_value == 200_000.0
        assert w.layers[1].margin_value == 100_000.0
        assert w.layers[2].margin_value == 50_000.0
        assert w.layers[3].margin_value == 20_000.0

    def test_null_pct_returns_null_value_not_fabricated_zero(self) -> None:
        row = CommercialSnapshot(
            actual_revenue=500_000,
            actual_cost=300_000,
            gross_margin_pct=0.40,
            contribution_margin_pct=None,
            portfolio_margin_pct=None,
            net_margin_pct=None,
        )
        w = compute_waterfall(row)
        assert w.layers[0].margin_pct == 0.40
        assert w.layers[0].margin_value == 200_000.0
        for layer in w.layers[1:]:
            assert layer.margin_pct is None
            assert layer.margin_value is None


class TestComputeBridge:
    def _phoenix_prior(self) -> CommercialSnapshot:
        # Phoenix Feb 2026 from M2 seed.
        return CommercialSnapshot(
            actual_revenue=845_000,
            actual_cost=555_000,
            gross_margin_pct=0.314,
            contribution_margin_pct=0.182,
            portfolio_margin_pct=0.108,
            net_margin_pct=0.062,
        )

    def _phoenix_current(self) -> CommercialSnapshot:
        # Phoenix Mar 2026 from M2 seed.
        return CommercialSnapshot(
            actual_revenue=820_000,
            actual_cost=590_000,
            gross_margin_pct=0.28,
            contribution_margin_pct=0.125,
            portfolio_margin_pct=0.082,
            net_margin_pct=0.041,
        )

    def _tier_set(self, rate_mult: float = 1.0, weight_shift: float = 0.0) -> list[TierSnapshot]:
        """Plausible three-tier snapshot for a test run."""
        return [
            TierSnapshot(
                role_tier="Junior",
                planned_rate=70.0,
                actual_rate=70.0 * rate_mult,
                tier_weight_planned=0.30,
                tier_weight_actual=0.40 + weight_shift,
            ),
            TierSnapshot(
                role_tier="Mid",
                planned_rate=110.0,
                actual_rate=118.0 * rate_mult,
                tier_weight_planned=0.50,
                tier_weight_actual=0.45 - weight_shift,
            ),
            TierSnapshot(
                role_tier="Senior",
                planned_rate=180.0,
                actual_rate=175.0 * rate_mult,
                tier_weight_planned=0.20,
                tier_weight_actual=0.15,
            ),
        ]

    def test_phoenix_feb_to_mar_total_delta_is_minus_340_bps(self) -> None:
        result = compute_bridge(
            prior=self._phoenix_prior(),
            current=self._phoenix_current(),
            tiers_prior=self._tier_set(rate_mult=1.0, weight_shift=0.0),
            tiers_current=self._tier_set(rate_mult=1.02, weight_shift=0.02),
        )
        assert abs(result.total_delta_bps - (-340.0)) < 1.0, (
            f"expected -340 bps, got {result.total_delta_bps}"
        )

    def test_drivers_sum_to_total_delta_exactly(self) -> None:
        result = compute_bridge(
            prior=self._phoenix_prior(),
            current=self._phoenix_current(),
            tiers_prior=self._tier_set(rate_mult=1.0, weight_shift=0.0),
            tiers_current=self._tier_set(rate_mult=1.02, weight_shift=0.02),
        )
        driver_sum = (
            result.drivers.price_bps
            + result.drivers.volume_bps
            + result.drivers.mix_bps
            + result.drivers.cost_bps_residual
        )
        assert abs(driver_sum - result.total_delta_bps) < 0.01

    def test_cost_is_residual_by_construction(self) -> None:
        # If we pass identical tier snapshots on both sides, Price and Mix
        # collapse to ~0 and Cost absorbs the full total (minus Volume).
        tiers = self._tier_set(rate_mult=1.0, weight_shift=0.0)
        result = compute_bridge(
            prior=self._phoenix_prior(),
            current=self._phoenix_current(),
            tiers_prior=tiers,
            tiers_current=tiers,
        )
        assert abs(result.drivers.price_bps) < 0.01
        assert abs(result.drivers.mix_bps) < 0.01
        # Volume and Cost together equal the total.
        assert abs(
            result.drivers.volume_bps + result.drivers.cost_bps_residual - result.total_delta_bps
        ) < 0.01

    def test_empty_tiers_still_ties_to_total(self) -> None:
        result = compute_bridge(
            prior=self._phoenix_prior(),
            current=self._phoenix_current(),
            tiers_prior=[],
            tiers_current=[],
        )
        assert result.drivers.price_bps == 0.0
        assert result.drivers.mix_bps == 0.0
        # Total still exact.
        driver_sum = (
            result.drivers.price_bps
            + result.drivers.volume_bps
            + result.drivers.mix_bps
            + result.drivers.cost_bps_residual
        )
        assert abs(driver_sum - result.total_delta_bps) < 0.01

    def test_phoenix_feb_to_mar_identity_price_mix_volume_cost_equal_total(
        self,
    ) -> None:
        """Locked identity from M3b mid-checkpoint: Price + Mix + Volume + Cost
        must equal total_delta_bps exactly for the PHOENIX Feb-Mar case.
        """
        # Exact Phoenix Feb and Mar tier snapshots as seeded by M2.
        tiers_feb = [
            TierSnapshot(
                role_tier="Junior",
                planned_rate=70.0,
                actual_rate=71.0,
                tier_weight_planned=0.30,
                tier_weight_actual=0.40,
            ),
            TierSnapshot(
                role_tier="Mid",
                planned_rate=110.0,
                actual_rate=114.0,
                tier_weight_planned=0.50,
                tier_weight_actual=0.415,
            ),
            TierSnapshot(
                role_tier="Senior",
                planned_rate=180.0,
                actual_rate=177.5,
                tier_weight_planned=0.20,
                tier_weight_actual=0.185,
            ),
        ]
        tiers_mar = [
            TierSnapshot(
                role_tier="Junior",
                planned_rate=70.0,
                actual_rate=72.0,
                tier_weight_planned=0.30,
                tier_weight_actual=0.50,
            ),
            TierSnapshot(
                role_tier="Mid",
                planned_rate=110.0,
                actual_rate=118.0,
                tier_weight_planned=0.50,
                tier_weight_actual=0.33,
            ),
            TierSnapshot(
                role_tier="Senior",
                planned_rate=180.0,
                actual_rate=175.0,
                tier_weight_planned=0.20,
                tier_weight_actual=0.17,
            ),
        ]
        result = compute_bridge(
            prior=self._phoenix_prior(),
            current=self._phoenix_current(),
            tiers_prior=tiers_feb,
            tiers_current=tiers_mar,
        )
        # Total must still reconcile to the M2 gate.
        assert abs(result.total_delta_bps - (-340.0)) < 1.0
        # Identity: four drivers sum exactly to the total. Rounding
        # to 2 decimal places on each component means the identity
        # holds to one-cent-of-a-bp.
        identity = (
            result.drivers.price_bps
            + result.drivers.mix_bps
            + result.drivers.volume_bps
            + result.drivers.cost_bps_residual
        )
        assert abs(identity - result.total_delta_bps) < 0.01
