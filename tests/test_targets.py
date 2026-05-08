import pytest

from agentic_starter import TargetType, normalize_target, normalize_targets

_VALID_253_CHAR_HOST = ("a" * 50 + ".") * 4 + "a" * 49
_INVALID_254_CHAR_HOST = _VALID_253_CHAR_HOST + "a"
_VALID_63_CHAR_LABEL = "a" * 63
_INVALID_64_CHAR_LABEL = "a" * 64


def test_normalize_target_ignores_comments_and_blank_lines() -> None:
    assert normalize_target("# comment") is None
    assert normalize_target("   ") is None


def test_normalize_target_classifies_ip_address_and_network() -> None:
    address = normalize_target("192.0.2.10")
    network = normalize_target("198.51.100.0/24")

    assert address is not None
    assert address.value == "192.0.2.10"
    assert address.target_type == TargetType.IP_ADDRESS

    assert network is not None
    assert network.value == "198.51.100.0/24"
    assert network.target_type == TargetType.IP_NETWORK


def test_normalize_target_lowercases_domains_without_network_lookup() -> None:
    target = normalize_target("Example.COM.")

    assert target is not None
    assert target.value == "example.com"
    assert target.target_type == TargetType.DOMAIN


def test_normalize_targets_deduplicates_preserving_order() -> None:
    targets = normalize_targets(
        [
            "Example.com",
            "example.com",
            "api.example.com",
            "192.0.2.10",
            "192.0.2.10",
        ]
    )

    assert [target.value for target in targets] == [
        "example.com",
        "api.example.com",
        "192.0.2.10",
    ]


@pytest.mark.parametrize(
    "value",
    [
        "http://example.com",
        "example.com:8080",
        "example.com/path",
        "foo..bar",
        "-foo.com",
        "foo-.com",
        "foo_bar.com",
        "not a host",
        "münchen.de",
    ],
)
def test_normalize_target_rejects_invalid_dns_inputs(value: str) -> None:
    assert normalize_target(value) is None


def test_normalize_target_accepts_253_char_host() -> None:
    target = normalize_target(_VALID_253_CHAR_HOST)

    assert target is not None
    assert target.value == _VALID_253_CHAR_HOST


def test_normalize_target_rejects_254_char_host() -> None:
    assert normalize_target(_INVALID_254_CHAR_HOST) is None


def test_normalize_target_accepts_63_char_single_label() -> None:
    target = normalize_target(_VALID_63_CHAR_LABEL)

    assert target is not None
    assert target.value == _VALID_63_CHAR_LABEL
    assert target.target_type == TargetType.HOSTNAME


def test_normalize_target_rejects_64_char_single_label() -> None:
    assert normalize_target(_INVALID_64_CHAR_LABEL) is None


def test_normalize_target_accepts_punycode_label() -> None:
    target = normalize_target("xn--mnchen-3ya.de")

    assert target is not None
    assert target.value == "xn--mnchen-3ya.de"
    assert target.target_type == TargetType.DOMAIN


def test_normalize_target_accepts_localhost_single_label() -> None:
    target = normalize_target("localhost")

    assert target is not None
    assert target.value == "localhost"
    assert target.target_type == TargetType.HOSTNAME

