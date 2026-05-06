"""Small example module with behavior that is easy for Claude to test and refactor."""

from __future__ import annotations

import re

_SEPARATOR_PATTERN = re.compile(r"[^a-z0-9]+")


def normalize_identifier(value: str) -> str:
    """Return a stable lowercase identifier from a human-readable string.

    The function is intentionally simple so Claude can practice adding tests,
    fixing edge cases, and refactoring without needing domain-specific context.
    """
    normalized = _SEPARATOR_PATTERN.sub("-", value.lower()).strip("-")
    return re.sub(r"-{2,}", "-", normalized)

