from agentic_starter import TargetType, normalize_target, normalize_targets


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

