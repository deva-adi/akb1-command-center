from __future__ import annotations

from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CurrencyRate


async def _seed_rates(session: AsyncSession) -> None:
    session.add_all(
        [
            CurrencyRate(code="USD", symbol="$", rate_to_base=Decimal("1.0"), source="seed"),
            CurrencyRate(code="INR", symbol="₹", rate_to_base=Decimal("83.5"), source="seed"),
            CurrencyRate(code="GBP", symbol="£", rate_to_base=Decimal("0.79"), source="seed"),
        ]
    )
    await session.commit()


@pytest.mark.asyncio
async def test_currency_rates_anchored_to_usd(
    session: AsyncSession, app_client: AsyncClient
) -> None:
    await _seed_rates(session)
    response = await app_client.get("/api/v1/currency/rates")
    assert response.status_code == 200
    rates = {row["code"]: row for row in response.json()}
    assert Decimal(rates["USD"]["rate_to_base"]) == Decimal("1.0")
    assert rates["USD"]["symbol"] == "$"
    assert Decimal(rates["INR"]["rate_to_base"]) == Decimal("83.5")
    # Rates should be sorted alphabetically by code
    codes = [row["code"] for row in response.json()]
    assert codes == sorted(codes)
