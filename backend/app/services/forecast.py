"""Forecasting primitives — linear regression, weighted MA, exponential smoothing.

Full wiring into the KPI pipeline lands in Iteration 3. The math itself is
kept dependency-free so it runs during tests without NumPy.
"""
from __future__ import annotations

from collections.abc import Sequence
from statistics import fmean


def linear_trend(values: Sequence[float], horizon: int = 1) -> list[float]:
    n = len(values)
    if n < 2 or horizon < 1:
        return [values[-1] if values else 0.0] * max(horizon, 0)
    xs = list(range(n))
    x_mean = fmean(xs)
    y_mean = fmean(values)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, values, strict=True))
    denominator = sum((x - x_mean) ** 2 for x in xs)
    slope = numerator / denominator if denominator else 0.0
    intercept = y_mean - slope * x_mean
    return [intercept + slope * (n + step) for step in range(horizon)]


def weighted_moving_average(values: Sequence[float], window: int = 3) -> float:
    if not values:
        return 0.0
    window = max(1, min(window, len(values)))
    tail = values[-window:]
    weights = list(range(1, window + 1))
    return sum(v * w for v, w in zip(tail, weights, strict=True)) / sum(weights)


def exponential_smoothing(values: Sequence[float], alpha: float = 0.4) -> float:
    if not values:
        return 0.0
    level = values[0]
    for value in values[1:]:
        level = alpha * value + (1 - alpha) * level
    return level
