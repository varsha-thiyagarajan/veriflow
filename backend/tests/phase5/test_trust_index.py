from backend.app.phase5.trust_index import (
    calculate_trust_index,
    calculate_grounding_accuracy,
    calculate_equivalence_pass_rate,
    calculate_hallucination_rate,
    calculate_trust_index_from_results,
)


def test_production_ready_trust_index():
    result = calculate_trust_index(
        grounding_accuracy=0.95,
        equivalence_pass_rate=0.95,
        hallucination_rate=0.05,
    )

    assert result["trust_index"] == 0.95
    assert result["trust_index_percent"] == 95.0
    assert result["decision"] == "PRODUCTION_READY"


def test_human_review_trust_index():
    result = calculate_trust_index(
        grounding_accuracy=0.80,
        equivalence_pass_rate=0.70,
        hallucination_rate=0.10,
    )

    assert result["trust_index"] == 0.78
    assert result["decision"] == "HUMAN_REVIEW"


def test_reject_trust_index():
    result = calculate_trust_index(
        grounding_accuracy=0.40,
        equivalence_pass_rate=0.30,
        hallucination_rate=0.50,
    )

    assert result["trust_index"] == 0.38
    assert result["decision"] == "REJECT_OR_REGENERATE"


def test_invalid_metric_above_one():
    try:
        calculate_trust_index(
            grounding_accuracy=1.1,
            equivalence_pass_rate=0.8,
            hallucination_rate=0.1,
        )
        assert False
    except ValueError:
        assert True


def test_invalid_metric_below_zero():
    try:
        calculate_trust_index(
            grounding_accuracy=0.8,
            equivalence_pass_rate=-0.1,
            hallucination_rate=0.1,
        )
        assert False
    except ValueError:
        assert True


def test_grounding_accuracy():
    claims = [
        {"claim_id": "C001", "verdict": "GROUNDED"},
        {"claim_id": "C002", "verdict": "GROUNDED"},
        {"claim_id": "C003", "verdict": "UNSUPPORTED"},
        {"claim_id": "C004", "verdict": "UNCERTAIN"},
    ]

    result = calculate_grounding_accuracy(claims)

    assert result == 0.5


def test_equivalence_pass_rate():
    tests = [
        {"test_id": "T001", "passed": True},
        {"test_id": "T002", "passed": True},
        {"test_id": "T003", "passed": False},
        {"test_id": "T004", "passed": True},
    ]

    result = calculate_equivalence_pass_rate(tests)

    assert result == 0.75


def test_hallucination_rate():
    claims = [
        {
            "claim_id": "C001",
            "evidence": [{"source_id": "DOC001"}],
        },
        {
            "claim_id": "C002",
            "evidence": [],
        },
        {
            "claim_id": "C003",
            "evidence": [{"source_id": "DOC002"}],
        },
        {
            "claim_id": "C004",
            "evidence": [],
        },
    ]

    result = calculate_hallucination_rate(claims)

    assert result == 0.5


def test_trust_index_from_results():
    claims = [
        {
            "claim_id": "C001",
            "verdict": "GROUNDED",
            "evidence": [{"source_id": "DOC001"}],
        },
        {
            "claim_id": "C002",
            "verdict": "GROUNDED",
            "evidence": [{"source_id": "DOC002"}],
        },
        {
            "claim_id": "C003",
            "verdict": "UNSUPPORTED",
            "evidence": [],
        },
        {
            "claim_id": "C004",
            "verdict": "GROUNDED",
            "evidence": [{"source_id": "DOC003"}],
        },
    ]

    tests = [
        {"test_id": "T001", "passed": True},
        {"test_id": "T002", "passed": True},
        {"test_id": "T003", "passed": False},
        {"test_id": "T004", "passed": True},
    ]

    result = calculate_trust_index_from_results(claims, tests)

    assert result["input_metrics"]["grounding_accuracy"] == 0.75
    assert result["input_metrics"]["equivalence_pass_rate"] == 0.75
    assert result["input_metrics"]["hallucination_rate"] == 0.25

    assert result["trust_index"] == 0.75
    assert result["decision"] == "HUMAN_REVIEW"


def test_empty_results():
    result = calculate_trust_index_from_results([], [])

    assert result["input_metrics"]["grounding_accuracy"] == 0.0
    assert result["input_metrics"]["equivalence_pass_rate"] == 0.0
    assert result["input_metrics"]["hallucination_rate"] == 0.0

    assert result["trust_index"] == 0.2
    assert result["decision"] == "REJECT_OR_REGENERATE"