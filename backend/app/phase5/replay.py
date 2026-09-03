import hashlib
import json
from typing import Any, Dict


def create_replay_record(
    artifact_id: str,
    artifact_type: str,
    input_data: Dict[str, Any],
    configuration: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Create a deterministic replay record for a verification run.
    """

    if configuration is None:
        configuration = {}

    input_json = json.dumps(
        input_data,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )

    input_hash = hashlib.sha256(
        input_json.encode("utf-8")
    ).hexdigest()

    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "input_hash": input_hash,
        "input_data": input_data,
        "configuration": configuration,
        "replay_command": (
            "python -m veriflow.replay "
            f"--artifact-id {artifact_id}"
        ),
    }


def verify_replay_input(
    replay_record: Dict[str, Any],
    input_data: Dict[str, Any],
) -> bool:
    """
    Verify that the supplied input matches the original
    replay record.
    """

    input_json = json.dumps(
        input_data,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )

    current_hash = hashlib.sha256(
        input_json.encode("utf-8")
    ).hexdigest()

    return current_hash == replay_record.get("input_hash")


def create_replay_instructions(
    replay_record: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create human-readable instructions for reproducing
    a verification run.
    """

    return {
        "artifact_id": replay_record.get("artifact_id"),
        "artifact_type": replay_record.get("artifact_type"),
        "input_hash": replay_record.get("input_hash"),
        "configuration": replay_record.get("configuration", {}),
        "replay_command": replay_record.get(
            "replay_command"
        ),
        "steps": [
            "Load the original verification input.",
            "Apply the recorded configuration.",
            "Run the VeriFlow verification pipeline.",
            "Compare the new results with the original audit report.",
        ],
    }