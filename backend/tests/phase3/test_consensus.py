from app.phase3.consensus import (
    calculate_consensus_score,
    calculate_claim_confidence,
    get_claim_verdict,
)


def test_consensus_score():
    score = calculate_consensus_score(
        agreeing_sources=3,
        total_sources=3,
        average_agreement_strength=0.9,
    )

    assert score == 0.9


def test_claim_confidence():
    confidence = calculate_claim_confidence(
        nli_entailment_probability=0.9,
        source_reliability=0.9,
        consensus_score=0.9,
    )

    assert confidence == 0.9


def test_grounded_verdict():
    verdict = get_claim_verdict(
        confidence=0.9,
        contradiction_probability=0.02,
    )

    assert verdict == "GROUNDED"


def test_uncertain_verdict():
    verdict = get_claim_verdict(
        confidence=0.7,
        contradiction_probability=0.1,
    )

    assert verdict == "UNCERTAIN"


def test_unsupported_verdict():
    verdict = get_claim_verdict(
        confidence=0.4,
        contradiction_probability=0.1,
    )

    assert verdict == "UNSUPPORTED"


def test_contradiction_takes_priority():
    verdict = get_claim_verdict(
        confidence=0.95,
        contradiction_probability=0.9,
    )

    assert verdict == "CONTRADICTED"