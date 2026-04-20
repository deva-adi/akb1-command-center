"""3-level metric aggregation (Project → Programme → Portfolio).

Full implementation planned for Iteration 2 (see docs/FORMULAS.md §1.x).
This module exposes the public API so other services can depend on it
without breaking when the richer rollups land.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class AggregatedMetric:
    scope: str
    code: str
    value: float
    sample_size: int


def weighted_mean(values: Iterable[float], weights: Iterable[float]) -> float:
    values_list = list(values)
    weights_list = list(weights)
    total_weight = sum(weights_list)
    if total_weight == 0 or not values_list:
        return 0.0
    return sum(v * w for v, w in zip(values_list, weights_list, strict=True)) / total_weight
