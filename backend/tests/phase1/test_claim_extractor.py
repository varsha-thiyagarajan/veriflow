from app.phase1.claim_extractor import extract_claims


def test_extract_claims_from_multiple_sentences():
    text = (
        "The system validates user input. "
        "Invalid requests are rejected."
    )

    claims = extract_claims(text)

    assert len(claims) == 2

    assert claims[0]["claim_id"] == "C001"
    assert claims[0]["sentence_id"] == "S001"
    assert claims[0]["claim_text"] == "The system validates user input."

    assert claims[1]["claim_id"] == "C002"
    assert claims[1]["sentence_id"] == "S002"
    assert claims[1]["claim_text"] == "Invalid requests are rejected."


def test_empty_text_returns_empty_list():
    assert extract_claims("") == []


def test_whitespace_text_returns_empty_list():
    assert extract_claims("   ") == []