"""
estimative_language.py
Kent-style estimative probability lexicon for osintmcp / claude-osint-agentic-starter.
"""
from __future__ import annotations

PROBABILITY: dict[str, tuple[int, int]] = {
    "almost certainly": (90, 99),
    "very likely":      (80, 90),
    "likely":           (60, 80),
    "roughly even":     (40, 60),
    "unlikely":         (20, 40),
    "remote":           (1,  20),
}

CONFIDENCE: dict[str, str] = {
    "high": (
        "Strong source access, strong credibility, "
        "meaningful corroboration, short inference chain."
    ),
    "moderate": (
        "Credible reporting but incomplete visibility, "
        "limited corroboration, or longer inference chain."
    ),
    "low": (
        "Plausible inference from thin, indirect, "
        "or weakly corroborated evidence."
    ),
}

EVIDENCE_LABELS: list[str] = [
    "source-observed",
    "reported",
    "assessed",
    "inferred",
]

CONFIDENCE_BASIS_SCHEMA: dict[str, list[str]] = {
    "source_access": [
        "direct_telemetry",
        "reverse_engineering",
        "vendor_incident_response",
        "government_statement",
        "official_record",
        "secondary_reporting",
    ],
    "source_reliability": ["established", "unknown", "contested", "mixed"],
    "information_credibility": ["corroborated", "single_source", "inferred", "disputed"],
    "author_verification": ["verified", "partially_verified", "not_verified"],
}

def label_probability(pct: int) -> str:
    """Return the correct estimative term for a given probability percentage."""
    for term, (low, high) in PROBABILITY.items():
        if low <= pct <= high:
            return term
    raise ValueError(f"Probability {pct}% is out of range 1-99.")

def label_confidence(level: str) -> str:
    """Validate and return a confidence level label."""
    level = level.lower()
    if level not in CONFIDENCE:
        raise ValueError(f"Confidence must be one of: {list(CONFIDENCE.keys())}")
    return level
