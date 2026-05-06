from agentic_starter import normalize_identifier


def test_normalize_identifier_lowercases_and_replaces_separators() -> None:
    assert normalize_identifier("Hello, Claude Code!") == "hello-claude-code"


def test_normalize_identifier_collapses_repeated_separators() -> None:
    assert normalize_identifier("alpha___beta...gamma") == "alpha-beta-gamma"


def test_normalize_identifier_strips_outer_separators() -> None:
    assert normalize_identifier("  /Scoped Value/  ") == "scoped-value"

