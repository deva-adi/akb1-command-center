from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings


def build_limiter() -> Limiter:
    settings = get_settings()
    return Limiter(
        key_func=get_remote_address,
        default_limits=[settings.rate_limit_read],
    )


limiter = build_limiter()
