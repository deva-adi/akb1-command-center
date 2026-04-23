"""Tests for the standard error envelope wired via install_error_handlers (M3a)."""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.api.v1.error_envelope import install_error_handlers
from app.api.v1.pnl_filters import FilterValidationError
from app.services.lineage_keys import LineageKeyError


def _build_test_app() -> FastAPI:
    """Tiny FastAPI app that raises the custom errors on demand.

    Avoids depending on the main application so these tests exercise only
    the envelope handlers. The main app wires the same handlers in
    ``create_app``, so behaviour is identical end-to-end.
    """
    app = FastAPI()
    install_error_handlers(app)

    @app.get("/raise-filter")
    async def _raise_filter() -> None:
        raise FilterValidationError("from", "expected YYYY-MM-DD, got 'nope'", value="nope")

    @app.get("/raise-lineage")
    async def _raise_lineage() -> None:
        raise LineageKeyError("bad.key", "unknown tab 'bad'")

    return app


@pytest.mark.asyncio
async def test_filter_validation_error_returns_standard_envelope_422() -> None:
    app = _build_test_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        r = await client.get("/raise-filter")
    assert r.status_code == 422
    body = r.json()
    assert body["error"]["code"] == "bad_filter_value"
    assert "expected YYYY-MM-DD" in body["error"]["message"]
    assert body["error"]["details"]["field"] == "from"
    assert body["error"]["details"]["value"] == "nope"


@pytest.mark.asyncio
async def test_lineage_key_error_returns_standard_envelope_422() -> None:
    app = _build_test_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        r = await client.get("/raise-lineage")
    assert r.status_code == 422
    body = r.json()
    assert body["error"]["code"] == "bad_lineage_key"
    assert body["error"]["details"]["key"] == "bad.key"
    assert body["error"]["details"]["reason"] == "unknown tab 'bad'"


@pytest.mark.asyncio
async def test_envelope_shape_has_error_and_filters_applied_keys_only() -> None:
    app = _build_test_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        r = await client.get("/raise-filter")
    body = r.json()
    assert set(body.keys()) == {"error", "filters_applied"}
    assert set(body["error"].keys()) == {"code", "message", "details"}
