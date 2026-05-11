"""
kent_report_schema.py
Structured output schema for Step 6 report generation in osintmcp.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional
import json


@dataclass
class ConfidenceBasis:
    source_access: str
    source_reliability: str
    information_credibility: str
    author_verification: str


@dataclass
class AnalyticLayer:
    technical_behavior: Optional[str] = None
    technical_evidence_label: str = "source-observed"
    tooling: Optional[str] = None
    tooling_evidence_label: str = "reported"
    actor_label: Optional[str] = None
    actor_label_evidence_label: str = "reported"
    attribution: Optional[str] = None
    attribution_probability: Optional[str] = None
    attribution_confidence: Optional[str] = None
    attribution_basis: Optional[ConfidenceBasis] = None
    intent: Optional[str] = None
    intent_probability: Optional[str] = None
    intent_confidence: Optional[str] = None
    intent_basis: Optional[ConfidenceBasis] = None


@dataclass
class AlternativeHypothesis:
    label: str
    description: str
    discriminating_evidence: str


@dataclass
class BiasCheck:
    confirmation_bias_check: str
    alternative_hypothesis: str
    mirror_imaging_check: str
    anchoring_check: str


@dataclass
class CollectionGap:
    description: str
    required_collection: str
    impact_if_unresolved: str


@dataclass
class Finding:
    finding_id: str
    title: str
    summary: str
    probability_language: str
    confidence: str
    confidence_basis: ConfidenceBasis
    analytic_layers: AnalyticLayer
    assumptions: list[str] = field(default_factory=list)
    alternatives: list[AlternativeHypothesis] = field(default_factory=list)
    bias_check: Optional[BiasCheck] = None
    collection_gaps: list[CollectionGap] = field(default_factory=list)
    change_indicators: list[str] = field(default_factory=list)
    defensive_implications: dict[str, str] = field(default_factory=lambda: {
        "tactical": "",
        "operational": "",
        "strategic": "",
    })


@dataclass
class KentReport:
    product_title: str
    primary_intelligence_requirement: str
    decision_context: str
    target: str
    analyst: str = "osintmcp-claude"
    findings: list[Finding] = field(default_factory=list)
    overall_confidence: str = "moderate"
    key_collection_gaps: list[str] = field(default_factory=list)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)


def build_confidence_basis(
    source_access: str = "secondary_reporting",
    source_reliability: str = "established",
    information_credibility: str = "single_source",
    author_verification: str = "not_verified",
) -> ConfidenceBasis:
    return ConfidenceBasis(
        source_access=source_access,
        source_reliability=source_reliability,
        information_credibility=information_credibility,
        author_verification=author_verification,
    )


def build_bias_check(
    confirmation: str = "",
    alternative: str = "",
    mirror: str = "",
    anchoring: str = "",
) -> BiasCheck:
    return BiasCheck(
        confirmation_bias_check=confirmation,
        alternative_hypothesis=alternative,
        mirror_imaging_check=mirror,
        anchoring_check=anchoring,
    )
