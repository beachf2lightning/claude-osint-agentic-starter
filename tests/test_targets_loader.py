from pathlib import Path

import pytest

from agentic_starter import TargetType, load_targets_from_file

EXAMPLE_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "osint-targets"
    / "authorized-scope.example.txt"
)


def test_load_targets_from_file_normalizes_and_dedupes(tmp_path: Path) -> None:
    path = tmp_path / "scope.txt"
    path.write_text(
        "Example.com\n"
        "example.com\n"
        "api.example.com\n"
        "192.0.2.10\n"
        "192.0.2.10\n"
        "198.51.100.0/24\n",
        encoding="utf-8",
    )

    targets = load_targets_from_file(path)

    assert [target.value for target in targets] == [
        "example.com",
        "api.example.com",
        "192.0.2.10",
        "198.51.100.0/24",
    ]


def test_load_targets_from_file_handles_bom_and_crlf(tmp_path: Path) -> None:
    path = tmp_path / "scope.txt"
    path.write_bytes(b"\xef\xbb\xbfExample.com\r\n# comment\r\n192.0.2.10\r\n")

    targets = load_targets_from_file(path)

    assert [target.value for target in targets] == ["example.com", "192.0.2.10"]


def test_load_targets_from_file_returns_empty_for_comments_only(tmp_path: Path) -> None:
    path = tmp_path / "scope.txt"
    path.write_text("# only comments\n# nothing here\n\n", encoding="utf-8")

    assert load_targets_from_file(path) == []


def test_load_targets_from_file_raises_for_missing_path(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_targets_from_file(tmp_path / "missing.txt")


def test_load_targets_from_file_raises_for_directory(tmp_path: Path) -> None:
    with pytest.raises(IsADirectoryError):
        load_targets_from_file(tmp_path)


def test_load_targets_from_file_accepts_path_inside_allowed_root(tmp_path: Path) -> None:
    inside = tmp_path / "inside"
    inside.mkdir()
    path = inside / "scope.txt"
    path.write_text("example.com\n", encoding="utf-8")

    targets = load_targets_from_file(path, allowed_root=inside)

    assert [target.value for target in targets] == ["example.com"]


def test_load_targets_from_file_rejects_symlink_escape(tmp_path: Path) -> None:
    inside = tmp_path / "inside"
    outside = tmp_path / "outside"
    inside.mkdir()
    outside.mkdir()
    secret = outside / "scope.txt"
    secret.write_text("example.com\n", encoding="utf-8")
    link = inside / "scope.txt"
    link.symlink_to(secret)

    with pytest.raises(ValueError, match="outside allowed_root"):
        load_targets_from_file(link, allowed_root=inside)


def test_load_targets_from_file_sets_source_to_resolved_path(tmp_path: Path) -> None:
    path = tmp_path / "scope.txt"
    path.write_text("example.com\n192.0.2.10\n", encoding="utf-8")

    targets = load_targets_from_file(path)

    assert {target.source for target in targets} == {str(path.resolve())}


def test_load_targets_from_file_respects_explicit_source(tmp_path: Path) -> None:
    path = tmp_path / "scope.txt"
    path.write_text("example.com\n192.0.2.10\n", encoding="utf-8")

    targets = load_targets_from_file(path, source="lab-scope")

    assert all(target.source == "lab-scope" for target in targets)


def test_load_targets_from_file_loads_example_fixture() -> None:
    targets = load_targets_from_file(EXAMPLE_FIXTURE)

    assert [(target.value, target.target_type) for target in targets] == [
        ("example.com", TargetType.DOMAIN),
        ("example.org", TargetType.DOMAIN),
        ("192.0.2.0/24", TargetType.IP_NETWORK),
        ("198.51.100.10", TargetType.IP_ADDRESS),
    ]
