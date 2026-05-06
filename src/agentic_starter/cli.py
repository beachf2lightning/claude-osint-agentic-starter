"""Command-line entry point for the starter package."""

from __future__ import annotations

import argparse

from agentic_starter.normalizer import normalize_identifier


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize text into a stable identifier.")
    parser.add_argument("value", help="Text to normalize.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    print(normalize_identifier(args.value))

