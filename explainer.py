"""Deterministic explanation layer for synthetic FRS inputs.

Render patient-facing and provider-facing explanations from the same 
approved score-level facts. Facts are audience-independent; audience 
only changes wording. No raw health information is added or inferred.
"""

import hashlib
import json

# Part 1

# allowed values: Sources from the Bounded Explanation Input Contract
ALLOWED_FIELDS = {
    "score_version", "explanation_version", "tier",
    "score", "contributors", "missing_domains", "case_id"
}
ALLOWED_TIERS = {"T1", "T2", "T3", "T4"}
SCORE_MIN = 0
SCORE_MAX = 100
ALLOWED_CONTRIBUTOR_DOMAINS = {"cycle_pattern", "sleep", "stress", "physical_health"}
ALLOWED_SIGNALS = { "supportive", "mixed", "needs_attention", "not_available"}
SUPPORTED_SCORE_VERSION = {"SYNTHETIC-1.0"}
SUPPORTED_EXPLANATION_VERSION = {"TEMPLATE-1.0"}
ALLOWED_AUDIENCES = {"patient", "provider"}

#Neutral, non-advice phrasing per domain. No forbidden words appear here.
DOMAIN_LABELS = {
    "cycle_pattern": "cycle pattern",
    "sleep": "sleep", 
    "stress": "stress",
    "physical_health": "physical health"
}
TIER_MEANING = {
    "T1": "a strongly supportive readiness pattern",
    "T2": "a broadly supportive pattern with some areas to watch",
    "T3": "a mixed pattern across several areas", 
    "T4": "several areas flagged for attention"
}
SIGNAL_LABELS = {
    "supportive": "appeared supportive",
    "mixed": "showed a mixed picture",
    "needs_attention": "showed less support", 
    "not_available": "had no data available"
}

# Aligned with docs/SAFETY_CONTRACT.md.
FORBIDDEN_PHRASES = {
    "you should", "we recommend", "consult", "seek care",
    "treatment", "diagnosis", "will become pregnant", "caused by",
}

class ExplanationError(ValueError):
    pass

# Part 2
# Defensive validation of the input contract. Reject anything not explicitly allowed.
def _validate(payload: dict, audience: str) -> None:
    """Reject anything the contract does not explicitly allow. (tests 4 & 5)"""
    if audience not in ALLOWED_AUDIENCES:
        raise ExplanationError(f"Unknown audience: {audience!r}")

    unknown = set(payload) - ALLOWED_FIELDS
    if unknown:
        raise ExplanationError(f"Unknown fields: {sorted(unknown)}")

    if payload.get("score_version") not in SUPPORTED_SCORE_VERSION:
        raise ExplanationError("Unsupported score version")

    if payload.get("explanation_version") not in SUPPORTED_EXPLANATION_VERSION:
        raise ExplanationError("Unsupported explanation version")

    if payload.get("tier") not in ALLOWED_TIERS:
        raise ExplanationError("Invalid tier")

    score = payload.get("score")
    if score is not None and not (isinstance(score, int) and SCORE_MIN <= score <= SCORE_MAX):
        raise ExplanationError("Invalid score")

    for c in payload.get("contributors", []):
        if c.get("domain") not in ALLOWED_CONTRIBUTOR_DOMAINS:
            raise ExplanationError("Unknown domain")
        if c.get("signal") not in ALLOWED_SIGNALS:
            raise ExplanationError("Unknown signal")
        if not isinstance(c.get("rank"), int) or c["rank"] < 1:
            raise ExplanationError("Invalid rank")

    for d in payload.get("missing_domains", []):
        if d not in ALLOWED_CONTRIBUTOR_DOMAINS:
            raise ExplanationError("Unknown missing domain")

# Part 3
# Audience-independent facts. Both audiences share this.
def _build_facts(payload: dict) -> dict:
    """Audience-independent facts. Both audiences share this."""
    ordered = sorted(payload.get("contributors", []), key=lambda c: c["rank"])
    return {
        "tier": payload["tier"],
        "ordered_domains": [c["domain"] for c in ordered],
        "domain_signals": {c["domain"]: c["signal"] for c in ordered},
        "missing_domains": list(payload.get("missing_domains", [])),
    }

# Part 4
# Implemented versioned template driven explanation. Same facts, different wording. Neutral phrasing only.
def _render_text(facts: dict, audience: str) -> str:
    """Same facts, different wording. Neutral phrasing only."""
    tier_phrase = TIER_MEANING[facts["tier"]]
    labeled = [DOMAIN_LABELS[d] for d in facts["ordered_domains"]]
    domain_str = ", ".join(labeled) if labeled else "no ranked areas"

    signal_bits = [
        f"{DOMAIN_LABELS[d]} {SIGNAL_LABELS[facts['domain_signals'][d]]}"
        for d in facts["ordered_domains"]
    ]
    signal_str = "; ".join(signal_bits)
    missing = ", ".join(DOMAIN_LABELS[d] for d in facts["missing_domains"])

    if audience == "patient":
        text = f"Your overall result reflects {tier_phrase}. "
        text += f"The areas that shaped this result, in order, were: {domain_str}. "
        if signal_str:
            text += f"By area: {signal_str}. "
        if missing:
            text += f"Some areas had no information available: {missing}."
    else:  # provider
        text = f"Score tier {facts['tier']} indicates {tier_phrase}. "
        text += f"Contributing domains, ranked: {domain_str}. "
        if signal_str:
            text += f"Signal by domain: {signal_str}. "
        if missing:
            text += f"Domains without available data: {missing}."
    return text.strip()

# Part 5
# Enforce the explanation safety contract. Scan output for forbidden phrases.
def _assert_safe(text: str) -> None:
    """Structural safety gate, not a disclaimer. Scan output for forbidden phrases."""
    lowered = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lowered:
            raise ExplanationError(f"Forbidden phrase in output: {phrase!r}")

# Part 6
# Produce an audit event for the explanation.
def _build_audit(payload: dict) -> dict:
    """Metadata only. No bounded payload, no timestamp -> deterministic."""
    canonical = json.dumps(payload, sort_keys=True).encode("utf-8")
    input_hash = hashlib.sha256(canonical).hexdigest()
    return {
        "case_id": payload.get("case_id"),
        "score_version": payload.get("score_version"),
        "explanation_version": payload.get("explanation_version"),
        "input_sha256": input_hash,
        "outcome": "rendered",
    }


