def calculate_consensus_score(
    nli_results,
) -> float:
    """
    Calculate authority-weighted consensus.

    Higher-reliability sources receive disproportionately
    greater influence, while contradictory evidence is
    still preserved and penalizes the consensus.
    """

    if not nli_results:
        return 0.0

    weights = [
        max(0.0, min(1.0, result.get("source_reliability", 0.0))) ** 2
        for result in nli_results
    ]

    total_weight = sum(weights)

    if total_weight <= 0:
        return 0.0

    weighted_support = sum(
        weight * result.get("entailment_probability", 0.0)
        for weight, result in zip(weights, nli_results)
    )

    weighted_contradiction = sum(
        weight * result.get("contradiction_probability", 0.0)
        for weight, result in zip(weights, nli_results)
    )

    support_score = weighted_support / total_weight
    contradiction_score = weighted_contradiction / total_weight

    consensus = support_score - contradiction_score

    return round(
        min(max(consensus, 0.0), 1.0),
        3,
    )

def calculate_claim_confidence(
    nli_entailment_probability: float,
    source_reliability: float,
    consensus_score: float,
) -> float:
    """
    Calculate claim-level grounding confidence.
    """

    confidence = (
        0.5 * nli_entailment_probability
        + 0.3 * source_reliability
        + 0.2 * consensus_score
    )

    return round(
        min(max(confidence, 0.0), 1.0),
        3,
    )


def get_claim_verdict(
    confidence: float,
    contradiction_probability: float,
    entailment_probability: float = 0.0,
) -> str:
    """
    Generate a claim verdict using support, contradiction,
    and overall confidence.
    """

    # A strong contradiction should win when there is
    # no meaningful supporting evidence.
    if (
        contradiction_probability >= 0.90
        and entailment_probability < 0.50
    ):
        return "CONTRADICTED"

    # Strong overall grounding.
    if confidence >= 0.85:
        return "GROUNDED"

    # Moderate evidence requires human review.
    if confidence >= 0.60:
        return "UNCERTAIN"

    # Low confidence with strong contradiction.
    if contradiction_probability >= 0.90:
        return "CONTRADICTED"

    return "UNSUPPORTED"