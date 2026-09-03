from app.verification_pipeline import run_text_verification_pipeline


def test_real_three_phase_pipeline():
    content = "Java HashMap allows null keys."

    result = run_text_verification_pipeline(
        content=content,
    )

    # -------------------------
    # Phase 1
    # -------------------------
    assert result["phase1"]["input_type"] == "text"
    assert len(result["phase1"]["claims"]) > 0

    claim = result["phase1"]["claims"][0]

    assert claim["claim_id"] == "C001"
    assert claim["claim_text"] == content

    # -------------------------
    # Phase 2
    # -------------------------
    assert len(result["phase2"]) > 0
    assert result["phase2"][0]["claim_id"] == "C001"
    assert len(result["phase2"][0]["evidence"]) > 0

    evidence = result["phase2"][0]["evidence"][0]

    assert evidence["source_id"].startswith("WEB-")
    assert evidence["url"]
    assert evidence["text"]
    assert "reliability" in evidence

    # -------------------------
    # Phase 3
    # -------------------------
    assert len(result["phase3"]) == 1

    verification = result["phase3"][0]

    assert verification["claim_id"] == "C001"
    assert "verdict" in verification
    assert "confidence" in verification
    assert "consensus_score" in verification
    assert "nli_results" in verification