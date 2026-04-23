"""Tests for the lineage key parser and vocabulary (M3a shared infra)."""
from __future__ import annotations

import pytest

from app.services.lineage_keys import (
    AGGREGATIONS,
    SLICES,
    TABS,
    LineageKey,
    LineageKeyError,
    is_valid,
    parse,
)


class TestParseHappyPath:
    def test_parses_pnl_gross_margin_programme_month(self) -> None:
        k = parse("pnl.gross_margin_pct.programme.month")
        assert isinstance(k, LineageKey)
        assert k.tab == "pnl"
        assert k.metric == "gross_margin_pct"
        assert k.slice == "programme"
        assert k.aggregation == "month"
        assert k.raw == "pnl.gross_margin_pct.programme.month"

    def test_parses_executive_utilisation_resource_current(self) -> None:
        k = parse("executive.utilisation.resource.current")
        assert k.tab == "executive"
        assert k.slice == "resource"
        assert k.aggregation == "current"

    def test_parses_delivery_cpi_programme_rolling_3m(self) -> None:
        k = parse("delivery.cpi.programme.rolling_3m")
        assert k.aggregation == "rolling_3m"

    def test_none_slice_and_aggregation_are_valid_literals(self) -> None:
        k = parse("pnl.dso.none.none")
        assert k.slice == "none"
        assert k.aggregation == "none"


class TestParseRejectsMalformed:
    def test_rejects_three_segments(self) -> None:
        with pytest.raises(LineageKeyError) as exc:
            parse("pnl.gross_margin_pct.programme")
        assert "4 dot-separated segments" in exc.value.reason

    def test_rejects_five_segments(self) -> None:
        with pytest.raises(LineageKeyError) as exc:
            parse("pnl.gross_margin_pct.programme.month.extra")
        assert "4 dot-separated segments" in exc.value.reason

    def test_rejects_empty_string(self) -> None:
        with pytest.raises(LineageKeyError):
            parse("")

    def test_rejects_uppercase_segment(self) -> None:
        with pytest.raises(LineageKeyError) as exc:
            parse("PNL.gross_margin_pct.programme.month")
        assert "lowercase" in exc.value.reason.lower()

    def test_rejects_hyphen_in_segment(self) -> None:
        with pytest.raises(LineageKeyError) as exc:
            parse("pnl.gross-margin.programme.month")
        assert "lowercase" in exc.value.reason.lower()

    def test_rejects_empty_segment(self) -> None:
        with pytest.raises(LineageKeyError):
            parse("pnl..programme.month")

    def test_rejects_unknown_tab(self) -> None:
        with pytest.raises(LineageKeyError) as exc:
            parse("madeup.cpi.programme.month")
        assert "unknown tab" in exc.value.reason.lower()

    def test_rejects_unknown_slice(self) -> None:
        with pytest.raises(LineageKeyError) as exc:
            parse("pnl.cpi.galaxy.month")
        assert "unknown slice" in exc.value.reason.lower()

    def test_rejects_unknown_aggregation(self) -> None:
        with pytest.raises(LineageKeyError) as exc:
            parse("pnl.cpi.programme.rolling_5y")
        assert "unknown aggregation" in exc.value.reason.lower()


class TestVocabulary:
    def test_all_twelve_tab_slugs_present(self) -> None:
        # Adi's Q4 locked this vocabulary on 2026-04-22.
        expected = {
            "pnl",
            "executive",
            "delivery",
            "risk",
            "flow",
            "financials",
            "ai",
            "bench",
            "commercial",
            "backlog",
            "scenario",
            "ops",
        }
        assert TABS == expected

    def test_slice_vocabulary_exact(self) -> None:
        assert SLICES == {
            "programme",
            "resource",
            "sprint",
            "month",
            "phase",
            "portfolio",
            "none",
        }

    def test_aggregation_vocabulary_exact(self) -> None:
        assert AGGREGATIONS == {
            "current",
            "month",
            "quarter",
            "ytd",
            "rolling_3m",
            "none",
        }


class TestIsValid:
    def test_is_valid_returns_true_on_good_key(self) -> None:
        assert is_valid("pnl.gross_margin_pct.programme.month") is True

    def test_is_valid_returns_false_on_bad_key(self) -> None:
        assert is_valid("bad") is False


class TestImmutability:
    def test_lineage_key_is_frozen(self) -> None:
        k = parse("pnl.gross_margin_pct.programme.month")
        with pytest.raises(Exception):
            k.tab = "executive"  # type: ignore[misc]
