from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CurrencyRateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    symbol: str | None = None
    # rate_to_base = how many units of `code` equal 1 unit of the USD base.
    # e.g. INR rate_to_base = 83.50 means "1 USD = 83.50 INR".
    rate_to_base: Decimal
    source: str
    last_updated: datetime
