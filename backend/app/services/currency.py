"""Multi-currency conversion — see ARCHITECTURE.md §13."""
from __future__ import annotations

from decimal import Decimal


class CurrencyConversionError(RuntimeError):
    """Raised when a currency code has no rate configured."""


def convert(amount: Decimal, rate_to_base: Decimal) -> Decimal:
    """Convert an amount from a currency into the configured base currency.

    Rates are stored as rate_to_base — multiply to get the base-denominated
    value.
    """
    if rate_to_base <= 0:
        raise CurrencyConversionError("rate_to_base must be positive")
    return Decimal(amount) * Decimal(rate_to_base)
