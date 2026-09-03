from backend.app.phase5.replay import (
    create_replay_record,
    verify_replay_input,
    create_replay_instructions,
)


def test_create_replay_record():
    input_data = {
        "claim": "The system supports authentication.",
        "version": "1.0",
    }

    configuration = {
        "nli_model": "deberta",
        "threshold": 0.85,
    }

    result = create_replay_record(
        artifact_id="ART001",
        artifact_type="TEXT",
        input_data=input_data,
        configuration=configuration,
    )

    assert result["artifact_id"] == "ART001"
    assert result["artifact_type"] == "TEXT"
    assert result["input_data"] == input_data
    assert result["configuration"] == configuration
    assert len(result["input_hash"]) == 64
    assert result["replay_command"] == (
        "python -m veriflow.replay --artifact-id ART001"
    )


def test_same_input_produces_same_hash():
    input_data = {
        "claim": "The system supports authentication.",
        "value": 100,
    }

    result1 = create_replay_record(
        "ART002",
        "TEXT",
        input_data,
    )

    result2 = create_replay_record(
        "ART002",
        "TEXT",
        input_data,
    )

    assert result1["input_hash"] == result2["input_hash"]


def test_different_input_produces_different_hash():
    result1 = create_replay_record(
        "ART003",
        "TEXT",
        {"value": 100},
    )

    result2 = create_replay_record(
        "ART003",
        "TEXT",
        {"value": 200},
    )

    assert result1["input_hash"] != result2["input_hash"]


def test_verify_matching_replay_input():
    input_data = {
        "claim": "The system supports authentication.",
        "value": 100,
    }

    record = create_replay_record(
        "ART004",
        "TEXT",
        input_data,
    )

    assert verify_replay_input(record, input_data) is True


def test_verify_changed_replay_input():
    original_input = {
        "claim": "The system supports authentication.",
        "value": 100,
    }

    changed_input = {
        "claim": "The system supports authentication.",
        "value": 200,
    }

    record = create_replay_record(
        "ART005",
        "TEXT",
        original_input,
    )

    assert verify_replay_input(record, changed_input) is False


def test_create_replay_instructions():
    record = create_replay_record(
        "ART006",
        "CODE",
        {"source": "example.py"},
        {"python_version": "3.12"},
    )

    instructions = create_replay_instructions(record)

    assert instructions["artifact_id"] == "ART006"
    assert instructions["artifact_type"] == "CODE"
    assert instructions["input_hash"] == record["input_hash"]
    assert instructions["configuration"] == {
        "python_version": "3.12"
    }

    assert len(instructions["steps"]) == 4
    assert instructions["replay_command"] == record["replay_command"]


def test_default_configuration():
    record = create_replay_record(
        "ART007",
        "TEXT",
        {"claim": "Example"},
    )

    assert record["configuration"] == {}


def test_nested_input_is_deterministic():
    input_data = {
        "claims": [
            {"id": "C001", "text": "First claim"},
            {"id": "C002", "text": "Second claim"},
        ],
        "metadata": {
            "version": "1.0",
            "language": "en",
        },
    }

    record = create_replay_record(
        "ART008",
        "TEXT",
        input_data,
    )

    assert verify_replay_input(record, input_data) is True