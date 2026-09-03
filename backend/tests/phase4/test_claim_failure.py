from backend.app.phase4.claim_failure import analyze_claim_failure


def test_no_evidence():
    result = analyze_claim_failure({
        "claim_id": "C001",
        "claim_text": "The system supports encryption.",
        "confidence": 0.30,
        "verdict": "UNSUPPORTED",
        "evidence": []
    })

    assert result["failed"] is True
    assert result["reason"] == "NO_EVIDENCE"


def test_contradiction():
    result = analyze_claim_failure({
        "claim_id": "C002",
        "claim_text": "The system uses encryption.",
        "confidence": 0.40,
        "verdict": "UNSUPPORTED",
        "evidence": [
            {
                "source_id": "DOC001",
                "source_reliability": 0.90,
                "nli_label": "contradiction",
                "nli_probability": 0.85
            }
        ]
    })

    assert result["failed"] is True
    assert result["reason"] == "CONTRADICTION"
    assert "DOC001" in result["contradicting_sources"]


def test_low_source_reliability():
    result = analyze_claim_failure({
        "claim_id": "C003",
        "claim_text": "The system is highly scalable.",
        "confidence": 0.50,
        "verdict": "UNSUPPORTED",
        "evidence": [
            {
                "source_id": "DOC002",
                "source_reliability": 0.40,
                "nli_label": "entailment",
                "nli_probability": 0.60
            }
        ]
    })

    assert result["failed"] is True
    assert result["reason"] == "LOW_SOURCE_RELIABILITY"


def test_consensus_mismatch():
    result = analyze_claim_failure({
        "claim_id": "C004",
        "claim_text": "The application supports three languages.",
        "confidence": 0.50,
        "verdict": "UNCERTAIN",
        "evidence": [
            {
                "source_id": "DOC003",
                "source_reliability": 0.90,
                "nli_label": "entailment",
                "nli_probability": 0.80
            },
            {
                "source_id": "DOC004",
                "source_reliability": 0.90,
                "nli_label": "contradiction",
                "nli_probability": 0.75
            }
        ]
    })

    assert result["failed"] is True
    assert result["reason"] == "CONTRADICTION"


def test_grounded_claim():
    result = analyze_claim_failure({
        "claim_id": "C005",
        "claim_text": "The system supports authentication.",
        "confidence": 0.92,
        "verdict": "GROUNDED",
        "evidence": [
            {
                "source_id": "DOC005",
                "source_reliability": 0.95,
                "nli_label": "entailment",
                "nli_probability": 0.94
            }
        ]
    })

    assert result["failed"] is False
    assert result["reason"] is None