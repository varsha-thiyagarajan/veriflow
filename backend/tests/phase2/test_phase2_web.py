from app.phase2.pipeline import run_phase2


def test_phase2_external_web_retrieval():
    claims = [
        {
            "claim_id": "C001",
            "claim_text": "Java HashMap allows null keys",
        }
    ]

    result = run_phase2(
        claims=claims,
        use_web=True,
    )

    assert len(result) == 1
    assert result[0]["claim_id"] == "C001"
    assert len(result[0]["evidence"]) > 0

    evidence = result[0]["evidence"][0]

    assert evidence["source_id"].startswith("WEB-")
    assert evidence["url"]
    assert evidence["text"]
    assert "reliability" in evidence