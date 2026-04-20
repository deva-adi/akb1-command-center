from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.logging_config import get_logger
from app.models import CurrencyRate
from app.rate_limit import limiter
from app.schemas.currency import CurrencyRateOut

router = APIRouter(prefix="/currency", tags=["currency"])
log = get_logger(__name__)

# Frankfurter returns ECB reference rates with USD base. Free, no API key.
# Container must have egress to api.frankfurter.dev:443 for refresh to work.
FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest"
SUPPORTED_CODES = ("INR", "GBP", "EUR", "USD")
_write_limit = get_settings().rate_limit_write


@router.get("/rates", response_model=list[CurrencyRateOut])
async def list_rates(session: AsyncSession = Depends(get_session)) -> list[CurrencyRate]:
    """Return configured FX rates relative to the USD base.

    Rates are seeded at install time. Call POST /currency/refresh to pull
    current rates from the European Central Bank feed via frankfurter.app.
    """
    result = await session.execute(select(CurrencyRate).order_by(CurrencyRate.code))
    return list(result.scalars().all())


@router.post("/refresh", response_model=list[CurrencyRateOut])
@limiter.limit(_write_limit)
async def refresh_rates(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> list[CurrencyRate]:
    """Pull the latest rates from frankfurter.app and persist them.

    Rates are always stored relative to USD (USD itself is 1.0). The
    upstream feed is a public ECB mirror — if egress is blocked the
    endpoint returns HTTP 502 with the upstream error so the UI can
    fall back to the seeded rates.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(
                FRANKFURTER_URL,
                params={
                    "from": "USD",
                    "to": ",".join(c for c in SUPPORTED_CODES if c != "USD"),
                },
            )
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPError as exc:
        log.warning("currency.refresh.failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Live FX feed unavailable. The dashboard keeps using the most "
                "recent stored rates. See docs/RUN_BOOK.md §5 for proxy config."
            ),
        ) from exc

    rates = payload.get("rates", {}) if isinstance(payload, dict) else {}
    if not rates:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="FX feed returned no rates.",
        )

    now = datetime.now(UTC)
    # USD anchor is always 1.0.
    rates_with_usd = {"USD": Decimal("1.0"), **{k: Decimal(str(v)) for k, v in rates.items()}}

    for code, rate_to_base in rates_with_usd.items():
        existing = await session.get(CurrencyRate, code)
        symbol_default = {"USD": "$", "INR": "₹", "GBP": "£", "EUR": "€"}.get(code, code)
        if existing is None:
            session.add(
                CurrencyRate(
                    code=code,
                    symbol=symbol_default,
                    rate_to_base=rate_to_base,
                    source="frankfurter",
                    last_updated=now,
                )
            )
        else:
            existing.rate_to_base = rate_to_base
            existing.source = "frankfurter"
            existing.last_updated = now

    await session.commit()
    log.info("currency.refresh.ok", count=len(rates_with_usd))

    result = await session.execute(select(CurrencyRate).order_by(CurrencyRate.code))
    return list(result.scalars().all())
