from backend.app.phase4.divergence_detector import detect_divergence


def test_matching_outputs():
    result = detect_divergence({
        "test_id": "T001",
        "passed": True,
        "legacy_output": {
            "total": 100,
            "tax": 18
        },
        "migrated_output": {
            "total": 100,
            "tax": 18
        }
    })

    assert result["diverged"] is False
    assert result["divergent_fields"] == []


def test_single_field_divergence():
    result = detect_divergence({
        "test_id": "T002",
        "passed": False,
        "legacy_output": {
            "total": 100,
            "tax": 18
        },
        "migrated_output": {
            "total": 100,
            "tax": 20
        }
    })

    assert result["diverged"] is True
    assert result["reason"] == "OUTPUT_MISMATCH"
    assert result["divergent_fields"] == ["tax"]

    assert result["differences"]["tax"]["legacy"] == 18
    assert result["differences"]["tax"]["migrated"] == 20


def test_multiple_field_divergence():
    result = detect_divergence({
        "test_id": "T003",
        "passed": False,
        "legacy_output": {
            "subtotal": 100,
            "tax": 18,
            "total": 118
        },
        "migrated_output": {
            "subtotal": 110,
            "tax": 20,
            "total": 130
        }
    })

    assert result["diverged"] is True
    assert set(result["divergent_fields"]) == {
        "subtotal",
        "tax",
        "total"
    }


def test_missing_output():
    result = detect_divergence({
        "test_id": "T004",
        "passed": False,
        "legacy_output": {
            "total": 100
        },
        "migrated_output": None
    })

    assert result["diverged"] is True
    assert result["reason"] == "MISSING_OUTPUT"


def test_non_dictionary_outputs():
    result = detect_divergence({
        "test_id": "T005",
        "passed": False,
        "legacy_output": 100,
        "migrated_output": 120
    })

    assert result["diverged"] is True
    assert result["reason"] == "OUTPUT_MISMATCH"
    assert result["divergent_fields"] == ["output"]


def test_matching_non_dictionary_outputs():
    result = detect_divergence({
        "test_id": "T006",
        "passed": True,
        "legacy_output": "SUCCESS",
        "migrated_output": "SUCCESS"
    })

    assert result["diverged"] is False
    assert result["divergent_fields"] == []