def calculate_consensus_score(
    agreeing_sources: int,
    total_sources: int,
    average_agreement_strength: float
) -> float:
    """
    Calculate multi-source consensus score.
    """

    if total_sources <= 0:
        return 0.0

    agreement_ratio = agreeing_sources / total_sources

    score = agreement_ratio * average_agreement_strength

    return round(min(max(score, 0.0), 1.0), 3)


def calculate_claim_confidence(
    nli_entailment_probability: float,
    source_reliability: float,
    consensus_score: float
) -> float:
    """
    Combine NLI, source reliability, and consensus.

    Weights:
        NLI        = 0.5
        Reliability = 0.3
        Consensus   = 0.2
    """

    confidence = (
        0.5 * nli_entailment_probability
        + 0.3 * source_reliability
        + 0.2 * consensus_score
    )

    return round(min(max(confidence, 0.0), 1.0), 3)


def get_claim_verdict(
    confidence: float,
    contradiction_probability: float
) -> str:
    """
    Convert confidence into a final claim verdict.

    Contradiction takes priority over confidence.
    """

    if contradiction_probability > 0.5:
        return "CONTRADICTED"

    if confidence >= 0.85:
        return "GROUNDED"

    if confidence >= 0.60:
        return "UNCERTAIN"

    return "UNSUPPORTED"