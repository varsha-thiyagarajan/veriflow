from typing import Any, Dict, List


def calculate_trust_index(
    grounding_accuracy: float,
    equivalence_pass_rate: float,
    hallucination_rate: float,
) -> Dict[str, Any]:
    """
    Calculate the VeriFlow Trust Index.

    Formula:

        Trust Index =
            0.4 * Grounding Accuracy
            + 0.4 * Equivalence Pass Rate
            + 0.2 * (1 - Hallucination Rate)

    All input values must be between 0.0 and 1.0.
    """

    values = {
        "grounding_accuracy": grounding_accuracy,
        "equivalence_pass_rate": equivalence_pass_rate,
        "hallucination_rate": hallucination_rate,
    }

    for name, value in values.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(
                f"{name} must be between 0.0 and 1.0"
            )

    trust_index = (
        0.4 * grounding_accuracy
        + 0.4 * equivalence_pass_rate
        + 0.2 * (1.0 - hallucination_rate)
    )

    if trust_index >= 0.90:
        decision = "PRODUCTION_READY"
    elif trust_index >= 0.70:
        decision = "HUMAN_REVIEW"
    else:
        decision = "REJECT_OR_REGENERATE"

    return {
        "trust_index": round(trust_index, 4),
        "trust_index_percent": round(trust_index * 100, 2),
        "decision": decision,
        "components": {
            "grounding_accuracy": grounding_accuracy,
            "equivalence_pass_rate": equivalence_pass_rate,
            "hallucination_rate": hallucination_rate,
            "grounding_contribution": round(
                0.4 * grounding_accuracy, 4
            ),
            "equivalence_contribution": round(
                0.4 * equivalence_pass_rate, 4
            ),
            "hallucination_contribution": round(
                0.2 * (1.0 - hallucination_rate), 4
            ),
        },
    }


def calculate_grounding_accuracy(
    claim_results: List[Dict[str, Any]],
) -> float:
    """
    Calculate the percentage of claims that are grounded.
    """

    if not claim_results:
        return 0.0

    grounded_count = sum(
        1
        for claim in claim_results
        if str(claim.get("verdict", "")).upper() == "GROUNDED"
    )

    return grounded_count / len(claim_results)


def calculate_equivalence_pass_rate(
    test_results: List[Dict[str, Any]],
) -> float:
    """
    Calculate the percentage of equivalence tests that passed.
    """

    if not test_results:
        return 0.0

    passed_count = sum(
        1
        for test in test_results
        if bool(test.get("passed", False))
    )

    return passed_count / len(test_results)


def calculate_hallucination_rate(
    claim_results: List[Dict[str, Any]],
) -> float:
    """
    Calculate the percentage of claims that have no supporting evidence.
    """

    if not claim_results:
        return 0.0

    hallucinated_count = sum(
        1
        for claim in claim_results
        if not claim.get("evidence")
    )

    return hallucinated_count / len(claim_results)


def calculate_trust_index_from_results(
    claim_results: List[Dict[str, Any]],
    test_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Calculate the Trust Index directly from claim and test results.
    """

    grounding_accuracy = calculate_grounding_accuracy(
        claim_results
    )

    equivalence_pass_rate = calculate_equivalence_pass_rate(
        test_results
    )

    hallucination_rate = calculate_hallucination_rate(
        claim_results
    )

    result = calculate_trust_index(
        grounding_accuracy,
        equivalence_pass_rate,
        hallucination_rate,
    )

    result["input_metrics"] = {
        "grounding_accuracy": grounding_accuracy,
        "equivalence_pass_rate": equivalence_pass_rate,
        "hallucination_rate": hallucination_rate,
    }

    return result