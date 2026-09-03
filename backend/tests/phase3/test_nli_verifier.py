from app.phase3.nli_verifier import verify_claim


def test_nli_entailment():
    evidence = "HashMap allows one null key and multiple null values."
    claim = "HashMap allows null keys."

    result = verify_claim(claim, evidence)

    assert result["verdict"] == "entailment"
    assert result["entailment_probability"] > 0.5


def test_nli_contradiction():
    evidence = "HashMap does not allow null keys."
    claim = "HashMap allows null keys."

    result = verify_claim(claim, evidence)

    assert result["verdict"] == "contradiction"
    assert result["contradiction_probability"] > 0.5


def test_nli_returns_all_probabilities():
    evidence = "Java HashMap permits null keys."
    claim = "HashMap supports null keys."

    result = verify_claim(claim, evidence)

    assert "entailment_probability" in result
    assert "neutral_probability" in result
    assert "contradiction_probability" in result