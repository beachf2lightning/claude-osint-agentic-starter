"""Offline-safe target normalization helpers for defensive OSINT workflows."""

from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class TargetType(StrEnum):
    """Supported target categories for authorized scope files."""

    DOMAIN = "domain"
    HOSTNAME = "hostname"
    IP_ADDRESS = "ip_address"
    IP_NETWORK = "ip_network"


@dataclass(frozen=True, slots=True)
class Target:
    """A normalized target from an authorized scope file."""

    value: str
    target_type: TargetType
    source: str = "authorized-scope"


def normalize_target(value: str) -> Target | None:
    """Normalize one target line without performing network lookups.

    Blank lines and comments return `None`. The function intentionally avoids DNS
    resolution, HTTP requests, or reachability checks so it is safe for offline tests.
    """
    candidate = value.strip()
    if not candidate or candidate.startswith("#"):
        return None

    lowered = candidate.lower().rstrip(".")

    try:
        if "/" in lowered:
            network = ipaddress.ip_network(lowered, strict=False)
            return Target(str(network), TargetType.IP_NETWORK)

        address = ipaddress.ip_address(lowered)
        return Target(str(address), TargetType.IP_ADDRESS)
    except ValueError:
        pass

    target_type = TargetType.DOMAIN if lowered.count(".") == 1 else TargetType.HOSTNAME
    return Target(lowered, target_type)


def normalize_targets(lines: list[str]) -> list[Target]:
    """Normalize and deduplicate target lines while preserving first-seen order."""
    seen: set[tuple[str, TargetType]] = set()
    normalized: list[Target] = []

    for line in lines:
        target = normalize_target(line)
        if target is None:
            continue

        key = (target.value, target.target_type)
        if key in seen:
            continue

        seen.add(key)
        normalized.append(target)

    return normalized


def load_targets_from_file(
    path: str | os.PathLike[str],
    *,
    allowed_root: str | os.PathLike[str] | None = None,
) -> list[Target]:
    """Load and normalize targets from a UTF-8 scope file (BOM/CRLF tolerant).

    When ``allowed_root`` is set, the resolved path must lie within it; this
    rejects symlink escapes and absolute paths outside the trusted directory.
    """
    resolved = Path(path).resolve(strict=True)
    if allowed_root is not None:
        root = Path(allowed_root).resolve(strict=True)
        if not resolved.is_relative_to(root):
            raise ValueError(f"path {resolved} is outside allowed_root {root}")
    if resolved.is_dir():
        raise IsADirectoryError(f"expected file, got directory: {resolved}")
    text = resolved.read_text(encoding="utf-8-sig")
    return normalize_targets(text.splitlines())

