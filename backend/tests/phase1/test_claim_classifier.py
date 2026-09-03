from app.phase1.claim_classifier import (
    FACTUAL,
    INFERENTIAL,
    NORMATIVE,
    classify_claim,
    classify_claim_object,
)


def test_factual_claim():
    claim = "The system validates user input."

    assert classify_claim(claim) == FACTUAL


def test_inferential_claim():
    claim = "Therefore, the system rejects invalid requests."

    assert classify_claim(claim) == INFERENTIAL


def test_normative_claim():
    claim = "The system must validate user input."

    assert classify_claim(claim) == NORMATIVE


def test_classify_claim_object():
    claim = {
        "claim_id": "C001",
        "sentence_id": "S001",
        "claim_text": "The system validates user input.",
    }

    result = classify_claim_object(claim)

    assert result["claim_id"] == "C001"
    assert result["sentence_id"] == "S001"
    assert result["claim_type"] == FACTUAL


def test_empty_claim_is_rejected():
    try:
        classify_claim("")
        assert False
    except ValueError:
        assert True