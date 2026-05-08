import json
from pathlib import Path

import pytest

from agentic_starter.cli import build_parser, main

FIXTURE_DIR = Path(__file__).parent / "fixtures"
SCOPE_SMALL = FIXTURE_DIR / "scope_small.txt"


def test_build_parser_accepts_normalize_subcommand() -> None:
    parser = build_parser()
    args = parser.parse_args(["normalize", "Hello World"])

    assert args.command == "normalize"
    assert args.value == "Hello World"


def test_build_parser_accepts_scope_subcommand() -> None:
    parser = build_parser()
    args = parser.parse_args(["scope", "path.txt", "--format", "jsonl"])

    assert args.command == "scope"
    assert args.path == "path.txt"
    assert args.format == "jsonl"
    assert args.allowed_root is None


def test_main_normalize_prints_lowercased_identifier(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main(["normalize", "Hello World"])
    captured = capsys.readouterr()

    assert rc == 0
    assert captured.out == "hello-world\n"


def test_main_bare_value_still_normalizes(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["Hello World"])
    captured = capsys.readouterr()

    assert rc == 0
    assert captured.out == "hello-world\n"


def test_main_scope_text_format(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["scope", str(SCOPE_SMALL)])
    captured = capsys.readouterr()

    assert rc == 0
    assert captured.out == (
        "domain\texample.com\n"
        "ip_address\t192.0.2.10\n"
        "ip_network\t198.51.100.0/24\n"
    )


def test_main_scope_jsonl_format(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["scope", str(SCOPE_SMALL), "--format", "jsonl"])
    captured = capsys.readouterr()

    assert rc == 0
    parsed = [json.loads(line) for line in captured.out.splitlines()]
    assert parsed == [
        {"value": "example.com", "target_type": "domain", "source": "authorized-scope"},
        {"value": "192.0.2.10", "target_type": "ip_address", "source": "authorized-scope"},
        {"value": "198.51.100.0/24", "target_type": "ip_network", "source": "authorized-scope"},
    ]


def test_main_scope_missing_path_returns_nonzero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = main(["scope", str(tmp_path / "missing.txt")])
    captured = capsys.readouterr()

    assert rc == 2
    assert captured.out == ""
    assert "error:" in captured.err


def test_main_scope_with_allowed_root_rejects_outside(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    inside = tmp_path / "inside"
    outside = tmp_path / "outside"
    inside.mkdir()
    outside.mkdir()
    target_file = outside / "scope.txt"
    target_file.write_text("example.com\n", encoding="utf-8")

    rc = main(["scope", str(target_file), "--allowed-root", str(inside)])
    captured = capsys.readouterr()

    assert rc == 2
    assert "outside allowed_root" in captured.err
