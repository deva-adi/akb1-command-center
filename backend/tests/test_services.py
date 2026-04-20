from __future__ import annotations

from decimal import Decimal

import pytest

from app.services.aggregation import weighted_mean
from app.services.currency import CurrencyConversionError, convert
from app.services.forecast import (
    exponential_smoothing,
    linear_trend,
    weighted_moving_average,
)
from app.services.narrative import render


def test_weighted_mean_with_zero_weights() -> None:
    assert weighted_mean([1.0, 2.0], [0.0, 0.0]) == 0.0


def test_weighted_mean_basic() -> None:
    assert weighted_mean([1.0, 2.0, 3.0], [1.0, 1.0, 1.0]) == pytest.approx(2.0)


def test_linear_trend_extrapolates_upward_series() -> None:
    result = linear_trend([1.0, 2.0, 3.0], horizon=2)
    assert result[0] == pytest.approx(4.0)
    assert result[1] == pytest.approx(5.0)


def test_weighted_moving_average_weights_recent_values_more() -> None:
    result = weighted_moving_average([10, 20, 30], window=3)
    assert result == pytest.approx((10 + 40 + 90) / 6)


def test_exponential_smoothing_tracks_latest() -> None:
    assert exponential_smoothing([10, 20, 30], alpha=0.5) == pytest.approx(
        0.5 * 30 + 0.5 * (0.5 * 20 + 0.5 * 10)
    )


def test_currency_convert_multiplies_by_rate() -> None:
    assert convert(Decimal("100"), Decimal("83.5")) == Decimal("8350.0")


def test_currency_convert_rejects_non_positive_rate() -> None:
    with pytest.raises(CurrencyConversionError):
        convert(Decimal("100"), Decimal("0"))


def test_narrative_render_substitutes_variables() -> None:
    template = "Portfolio margin {margin}% across {count} programmes"
    assert render(template, {"margin": 13.8, "count": 5}) == (
        "Portfolio margin 13.8% across 5 programmes"
    )


def test_narrative_render_raises_on_missing_variable() -> None:
    with pytest.raises(ValueError):
        render("Hello {name}", {})
