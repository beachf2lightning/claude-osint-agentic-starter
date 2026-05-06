"""Starter package for Claude-assisted coding workflows."""

from agentic_starter.normalizer import normalize_identifier
from agentic_starter.targets import (
    Target,
    TargetType,
    load_targets_from_file,
    normalize_target,
    normalize_targets,
)

__all__ = [
    "Target",
    "TargetType",
    "load_targets_from_file",
    "normalize_identifier",
    "normalize_target",
    "normalize_targets",
]
