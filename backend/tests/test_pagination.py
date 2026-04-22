"""Tests for the pagination helper (M3a shared infra)."""
from __future__ import annotations

import pytest

from app.services.pagination import Page, paginate, pagination_from_counts


class TestPaginateInMemory:
    def test_first_page_returns_expected_slice(self) -> None:
        items = list(range(10))
        sliced, meta = paginate(items, Page(limit=3, offset=0))
        assert sliced == [0, 1, 2]
        assert meta.total == 10
        assert meta.returned == 3
        assert meta.limit == 3
        assert meta.offset == 0

    def test_second_page_advances_offset(self) -> None:
        items = list(range(10))
        sliced, meta = paginate(items, Page(limit=3, offset=3))
        assert sliced == [3, 4, 5]
        assert meta.returned == 3
        assert meta.offset == 3

    def test_offset_past_end_returns_empty(self) -> None:
        items = list(range(5))
        sliced, meta = paginate(items, Page(limit=3, offset=10))
        assert sliced == []
        assert meta.returned == 0
        assert meta.total == 5

    def test_limit_larger_than_total_returns_all(self) -> None:
        items = list(range(3))
        sliced, meta = paginate(items, Page(limit=100, offset=0))
        assert sliced == items
        assert meta.returned == 3


class TestPaginationFromCounts:
    def test_metadata_shape_for_sql_paginated_query(self) -> None:
        meta = pagination_from_counts(Page(limit=50, offset=100), total=237, returned=50)
        assert meta.limit == 50
        assert meta.offset == 100
        assert meta.total == 237
        assert meta.returned == 50


class TestPaginationDependency:
    """The dependency's ``Query(default=...)`` defaults only resolve when
    FastAPI invokes it via HTTP. Direct unit-test invocation receives the
    Query sentinels, not the ints. We validate HTTP behaviour via a tiny
    mounted app so the end-to-end resolution path is covered.
    """

    @pytest.mark.asyncio
    async def test_dependency_returns_page_with_explicit_values(self) -> None:
        from app.services.pagination import pagination_dependency

        page = await pagination_dependency(limit=25, offset=75)
        assert page.limit == 25
        assert page.offset == 75

    @pytest.mark.asyncio
    async def test_dependency_defaults_resolve_over_http(self) -> None:
        from fastapi import Depends, FastAPI
        from httpx import ASGITransport, AsyncClient

        from app.services.pagination import Page, pagination_dependency

        app = FastAPI()

        @app.get("/probe")
        async def _probe(page: Page = Depends(pagination_dependency)) -> dict[str, int]:
            return {"limit": page.limit, "offset": page.offset}

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
            r = await client.get("/probe")
        assert r.status_code == 200
        assert r.json() == {"limit": 50, "offset": 0}

    @pytest.mark.asyncio
    async def test_dependency_rejects_out_of_range_limit_with_422(self) -> None:
        from fastapi import Depends, FastAPI
        from httpx import ASGITransport, AsyncClient

        from app.api.v1.error_envelope import install_error_handlers
        from app.services.pagination import Page, pagination_dependency

        app = FastAPI()
        install_error_handlers(app)

        @app.get("/probe")
        async def _probe(page: Page = Depends(pagination_dependency)) -> dict[str, int]:
            return {"limit": page.limit}

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
            r = await client.get("/probe", params={"limit": 10000})
        assert r.status_code == 422
        body = r.json()
        assert body["error"]["code"] == "request_validation_failed"
