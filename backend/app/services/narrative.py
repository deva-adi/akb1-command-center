"""Template-based narrative generation — see ARCHITECTURE.md §12."""
from __future__ import annotations

from collections.abc import Mapping


def render(template: str, context: Mapping[str, object]) -> str:
    try:
        return template.format_map(context)
    except KeyError as exc:
        missing = exc.args[0] if exc.args else "unknown"
        raise ValueError(f"Missing narrative variable: {missing}") from exc
