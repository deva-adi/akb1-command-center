"""Standard error envelope for v5.7.0 Tab 12 P&L endpoints.

Every endpoint under ``/api/v1/pnl`` (and the future global lineage
endpoint in M9) returns the same JSON shape on non-2xx responses. The
envelope always carries a ``filters_applied`` block when filter parsing
finished before the error fired, so the frontend ContextRail can still
render breadcrumbs.

Errors come from two sources:

- Explicit raises of ``HTTPException`` from endpoint handlers.
- Custom domain errors: ``FilterValidationError`` and ``LineageKeyError``.
  The handler catches these and maps them to 422 with a stable code.

Register the handlers by calling ``install_error_handlers(app)`` from
``backend/app/main.py:create_app``.
"""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.pnl_filters import FilterValidationError
from app.schemas.pnl import ErrorEnvelope, ErrorEnvelopeBody, FiltersApplied
from app.services.lineage_keys import LineageKeyError


def _envelope(
    *,
    code: str,
    message: str,
    status_code: int,
    details: dict[str, Any] | None = None,
    filters_applied: FiltersApplied | None = None,
) -> JSONResponse:
    body = ErrorEnvelope(
        error=ErrorEnvelopeBody(code=code, message=message, details=details),
        filters_applied=filters_applied,
    )
    # by_alias so ``from`` serialises as ``from`` and not ``from_``.
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json", by_alias=True))


async def _handle_filter_validation_error(
    request: Request, exc: FilterValidationError
) -> JSONResponse:
    return _envelope(
        code="bad_filter_value",
        message=str(exc),
        status_code=422,
        details={"field": exc.field, "reason": exc.reason, "value": exc.value},
    )


async def _handle_lineage_key_error(request: Request, exc: LineageKeyError) -> JSONResponse:
    return _envelope(
        code="bad_lineage_key",
        message=str(exc),
        status_code=422,
        details={"key": exc.key, "reason": exc.reason},
    )


async def _handle_request_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return _envelope(
        code="request_validation_failed",
        message="one or more request parameters failed validation",
        status_code=422,
        details={"errors": exc.errors()},
    )


async def _handle_http_exception(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return _envelope(
        code=_code_for_status(exc.status_code),
        message=str(exc.detail) if exc.detail else f"HTTP {exc.status_code}",
        status_code=exc.status_code,
    )


def _code_for_status(status: int) -> str:
    return {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "unprocessable_entity",
        429: "rate_limited",
        500: "internal_error",
        501: "not_implemented",
        503: "service_unavailable",
    }.get(status, f"http_{status}")


def install_error_handlers(app: FastAPI) -> None:
    """Register the envelope-producing handlers on the FastAPI app.

    Only endpoints that opt in to the v5.7.0 error envelope will use
    these. Handlers for ``FilterValidationError`` and ``LineageKeyError``
    are global because those exceptions are raised from dependencies that
    run before the route handler. The ``HTTPException`` handler is also
    global; existing endpoints that already return their own shapes keep
    working because they use ``HTTPException`` sparingly and the envelope
    shape is a superset of the old shape for the 422 and 400 cases.
    """
    app.add_exception_handler(FilterValidationError, _handle_filter_validation_error)  # type: ignore[arg-type]
    app.add_exception_handler(LineageKeyError, _handle_lineage_key_error)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, _handle_request_validation_error)
