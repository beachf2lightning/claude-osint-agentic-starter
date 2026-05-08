"""Command-line entry point for the starter package."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from agentic_starter.normalizer import normalize_identifier
from agentic_starter.targets import Target, load_targets_from_file

KNOWN_SUBCOMMANDS = frozenset({"normalize", "scope"})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Defensive OSINT helpers: normalize identifiers and load authorized scope files."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    normalize_parser = subparsers.add_parser(
        "normalize",
        help="Normalize text into a stable identifier.",
    )
    normalize_parser.add_argument("value", help="Text to normalize.")

    scope_parser = subparsers.add_parser(
        "scope",
        help="Load and normalize an authorized-scope file (offline, no DNS or network).",
    )
    scope_parser.add_argument("path", help="Path to a scope file.")
    scope_parser.add_argument(
        "--format",
        choices=("text", "jsonl"),
        default="text",
        help="Output format (default: text).",
    )
    scope_parser.add_argument(
        "--allowed-root",
        default=None,
        help=(
            "Confine reads to this directory; rejects symlink escapes "
            "and absolute paths outside it."
        ),
    )

    return parser


def _handle_normalize(args: argparse.Namespace) -> int:
    print(normalize_identifier(args.value))
    return 0


def _handle_scope(args: argparse.Namespace) -> int:
    try:
        targets = load_targets_from_file(args.path, allowed_root=args.allowed_root)
    except (FileNotFoundError, IsADirectoryError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "jsonl":
        for target in targets:
            print(json.dumps(_target_as_dict(target)))
    else:
        for target in targets:
            print(f"{target.target_type}\t{target.value}")
    return 0


def _target_as_dict(target: Target) -> dict[str, str]:
    return {
        "value": target.value,
        "target_type": str(target.target_type),
        "source": target.source,
    }


def main(argv: Sequence[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if raw and not raw[0].startswith("-") and raw[0] not in KNOWN_SUBCOMMANDS:
        raw = ["normalize", *raw]

    parser = build_parser()
    args = parser.parse_args(raw)

    if args.command == "normalize":
        return _handle_normalize(args)
    return _handle_scope(args)
