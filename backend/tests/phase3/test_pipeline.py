from app.phase3.pipeline import (
    run_text_verification,
    run_code_verification,
)


def test_text_verification_without_evidence():
    claims = [
        {
            "claim_id": "C001",
            "claim_text": "HashMap allows null keys",
            "evidence": [],
        }
    ]

    result = run_text_verification(claims)

    assert len(result) == 1
    assert result[0]["claim_id"] == "C001"
    assert result[0]["verdict"] == "UNSUPPORTED"
    assert result[0]["confidence"] == 0.0


def test_code_verification_pass():
    test_cases = [
        {
            "test_id": "T001",
            "legacy_output": {"tax": 1250},
            "migrated_output": {"tax": 1250},
        }
    ]

    result = run_code_verification(test_cases)

    assert result["total_tests"] == 1
    assert result["passed_tests"] == 1
    assert result["pass_rate"] == 1.0
    assert result["verdict"] == "PASS"


def test_code_verification_fail():
    test_cases = [
        {
            "test_id": "T001",
            "legacy_output": {"tax": 1250},
            "migrated_output": {"tax": 1251},
        }
    ]

    result = run_code_verification(test_cases)

    assert result["total_tests"] == 1
    assert result["passed_tests"] == 0
    assert result["pass_rate"] == 0.0
    assert result["verdict"] == "FAIL"