"""Offline-safe target normalization helpers for defensive OSINT workflows."""

from __future__ import annotations

import ipaddress
import os
import re
from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path

_DNS_LABEL_PATTERN = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")


def _is_valid_dns_name(name: str) -> bool:
    if not 1 <= len(name) <= 253:
        return False
    if "/" in name or ":" in name:
        return False
    labels = name.split(".")
    return all(_DNS_LABEL_PATTERN.match(label) is not None for label in labels)


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

    if not _is_valid_dns_name(lowered):
        return None

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
    source: str | None = None,
) -> list[Target]:
    """Load and normalize targets from a UTF-8 scope file (BOM/CRLF tolerant).

    When ``allowed_root`` is set, the resolved path must lie within it; this
    rejects symlink escapes and absolute paths outside the trusted directory.
    When ``source`` is None, each returned target's ``source`` is the file's
    resolved absolute path; pass ``source`` to override.
    """
    resolved = Path(path).resolve(strict=True)
    if allowed_root is not None:
        root = Path(allowed_root).resolve(strict=True)
        if not resolved.is_relative_to(root):
            raise ValueError(f"path {resolved} is outside allowed_root {root}")
    if resolved.is_dir():
        raise IsADirectoryError(f"expected file, got directory: {resolved}")
    text = resolved.read_text(encoding="utf-8-sig")
    targets = normalize_targets(text.splitlines())
    effective_source = source if source is not None else str(resolved)
    return [replace(target, source=effective_source) for target in targets]

