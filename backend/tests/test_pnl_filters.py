"""Tests for the universal filter parser and alias handling (M3a)."""
from __future__ import annotations

from datetime import date
from unittest.mock import Mock

import pytest

from app.api.v1.pnl_filters import (
    FilterValidationError,
    PnlFilters,
    pnl_filters_dependency,
)


def _mock_request(query: dict[str, str] | None = None) -> Mock:
    """Build a mock Request whose query_params behaves like a dict."""
    req = Mock()
    req.query_params = query or {}
    return req


async def _parse(**kwargs: object) -> PnlFilters:
    """Drive the FastAPI dependency directly with keyword args.

    Any aliases must be passed via the ``query`` kwarg so they land on
    ``request.query_params``. Canonical params go through the named
    dependency arguments.
    """
    query_params = kwargs.pop("query", {})
    request = _mock_request(query=query_params)
    return await pnl_filters_dependency(
        request=request,  # type: ignore[arg-type]
        programme=kwargs.get("programme"),  # type: ignore[arg-type]
        from_=kwargs.get("from_"),  # type: ignore[arg-type]
        to=kwargs.get("to"),  # type: ignore[arg-type]
        tier=kwargs.get("tier"),  # type: ignore[arg-type]
        scenario_name=kwargs.get("scenario_name"),  # type: ignore[arg-type]
        portfolio=kwargs.get("portfolio"),  # type: ignore[arg-type]
        month=kwargs.get("month"),  # type: ignore[arg-type]
    )


class TestEmptyAndCanonical:
    @pytest.mark.asyncio
    async def test_empty_query_returns_all_none(self) -> None:
        f = await _parse()
        assert f.programmes is None
        assert f.date_from is None
        assert f.date_to is None
        assert f.tier is None
        assert f.scenario_name is None
        assert f.portfolio is None
        assert f.month is None

    @pytest.mark.asyncio
    async def test_canonical_values_parse(self) -> None:
        f = await _parse(
            programme="PHOENIX",
            from_="2026-02-01",
            to="2026-03-01",
            tier="Junior",
            scenario_name="Monthly Actuals",
            portfolio="ENTERPRISE",
            month="2026-03-01",
        )
        assert f.programmes == ("PHOENIX",)
        assert f.date_from == date(2026, 2, 1)
        assert f.date_to == date(2026, 3, 1)
        assert f.tier == "Junior"
        assert f.scenario_name == "Monthly Actuals"
        assert f.portfolio == "ENTERPRISE"
        assert f.month == date(2026, 3, 1)

    @pytest.mark.asyncio
    async def test_programme_list_is_comma_split_and_uppercased(self) -> None:
        f = await _parse(programme="phoenix, atlas,bharat")
        assert f.programmes == ("PHOENIX", "ATLAS", "BHARAT")


class TestAliasAcceptance:
    @pytest.mark.asyncio
    async def test_programme_code_alias_resolves_to_programme(self) -> None:
        f = await _parse(query={"programme_code": "phoenix"})
        assert f.programmes == ("PHOENIX",)

    @pytest.mark.asyncio
    async def test_period_start_and_period_end_aliases_resolve(self) -> None:
        f = await _parse(query={"period_start": "2026-02-01", "period_end": "2026-03-31"})
        assert f.date_from == date(2026, 2, 1)
        assert f.date_to == date(2026, 3, 31)

    @pytest.mark.asyncio
    async def test_canonical_wins_when_both_forms_present(self) -> None:
        f = await _parse(
            programme="ATLAS",
            query={"programme_code": "PHOENIX"},
        )
        assert f.programmes == ("ATLAS",)


class TestValidation:
    @pytest.mark.asyncio
    async def test_bad_date_raises_422(self) -> None:
        with pytest.raises(FilterValidationError) as exc:
            await _parse(from_="not-a-date")
        assert exc.value.field == "from"

    @pytest.mark.asyncio
    async def test_unknown_tier_raises(self) -> None:
        with pytest.raises(FilterValidationError) as exc:
            await _parse(tier="Architect")
        assert exc.value.field == "tier"

    @pytest.mark.asyncio
    async def test_short_tier_forms_normalise(self) -> None:
        f_jr = await _parse(tier="Jr")
        f_sr = await _parse(tier="sr")
        assert f_jr.tier == "Junior"
        assert f_sr.tier == "Senior"

    @pytest.mark.asyncio
    async def test_invalid_programme_characters_rejected(self) -> None:
        with pytest.raises(FilterValidationError) as exc:
            await _parse(programme="PHOENIX!")
        assert exc.value.field == "programme"

    @pytest.mark.asyncio
    async def test_long_scenario_name_rejected(self) -> None:
        with pytest.raises(FilterValidationError):
            await _parse(scenario_name="x" * 200)


class TestAppliedBlockEmitsCanonicalOnly:
    @pytest.mark.asyncio
    async def test_applied_block_never_carries_alias_keys(self) -> None:
        f = await _parse(query={"programme_code": "PHOENIX", "period_start": "2026-02-01"})
        applied = f.to_applied_block()
        assert "programme" in applied
        assert "from" in applied
        assert "programme_code" not in applied
        assert "period_start" not in applied
        assert "period_end" not in applied

    @pytest.mark.asyncio
    async def test_applied_block_dates_emit_as_iso_strings(self) -> None:
        f = await _parse(from_="2026-02-01", to="2026-03-01")
        applied = f.to_applied_block()
        assert applied["from"] == "2026-02-01"
        assert applied["to"] == "2026-03-01"
