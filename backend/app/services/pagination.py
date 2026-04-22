"""Pagination helper shared across v5.7.0 Tab 12 list endpoints.

Offset-based pagination keeps URLs deep-linkable and shareable, which is
a hard requirement for M9 drill-across. Cursor pagination is avoided
deliberately because it does not survive URL copy-paste.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, TypeVar

from fastapi import Query

from app.schemas.pnl import Pagination

_DEFAULT_LIMIT = 50
_MAX_LIMIT = 500

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Page:
    """Parsed pagination request."""

    limit: int
    offset: int


async def pagination_dependency(
    limit: int = Query(default=_DEFAULT_LIMIT, ge=1, le=_MAX_LIMIT),
    offset: int = Query(default=0, ge=0),
) -> Page:
    """FastAPI dependency that parses ``?limit=50&offset=0``.

    FastAPI's ``ge``/``le`` constraints produce ``RequestValidationError``
    which the standard error envelope catches and returns as 422 with a
    stable ``request_validation_failed`` code.
    """
    return Page(limit=limit, offset=offset)


def paginate(items: Sequence[T], page: Page) -> tuple[list[T], Pagination]:
    """Slice ``items`` by ``page`` and produce the pagination metadata.

    Meant for already-in-memory collections; large queries should push
    ``limit``/``offset`` into the SQL statement and pass the unpaginated
    total via the ``total`` kwarg of ``Pagination`` directly.
    """
    total = len(items)
    sliced = list(items[page.offset : page.offset + page.limit])
    meta = Pagination(
        limit=page.limit,
        offset=page.offset,
        total=total,
        returned=len(sliced),
    )
    return sliced, meta


def pagination_from_counts(page: Page, total: int, returned: int) -> Pagination:
    """Build pagination metadata when the slice is already applied in SQL."""
    return Pagination(limit=page.limit, offset=page.offset, total=total, returned=returned)
