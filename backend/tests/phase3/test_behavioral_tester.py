from app.phase3.behavioral_tester import compare_outputs


def test_outputs_match():
    legacy = {
        "tax": 1250,
        "status": "SUCCESS"
    }

    migrated = {
        "tax": 1250,
        "status": "SUCCESS"
    }

    result = compare_outputs(legacy, migrated)

    assert result["verdict"] == "PASS"
    assert result["equal"] is True
    assert result["differences"] == []


def test_outputs_differ():
    legacy = {
        "tax": 1250,
        "status": "SUCCESS"
    }

    migrated = {
        "tax": 1251,
        "status": "SUCCESS"
    }

    result = compare_outputs(legacy, migrated)

    assert result["verdict"] == "FAIL"
    assert result["equal"] is False
    assert len(result["differences"]) == 1
    assert result["differences"][0]["field"] == "tax"
    assert result["differences"][0]["legacy_value"] == 1250
    assert result["differences"][0]["migrated_value"] == 1251


def test_non_dictionary_outputs():
    legacy = 100
    migrated = 101

    result = compare_outputs(legacy, migrated)

    assert result["verdict"] == "FAIL"
    assert result["differences"][0]["field"] == "output"