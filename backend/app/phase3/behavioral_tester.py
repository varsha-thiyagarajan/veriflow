from typing import Any, Dict, List


def compare_outputs(
    legacy_output: Any,
    migrated_output: Any
) -> Dict[str, Any]:
    """
    Compare legacy and migrated outputs.

    Returns PASS when outputs are identical.
    Returns FAIL with the exact differences otherwise.
    """

    if legacy_output == migrated_output:
        return {
            "verdict": "PASS",
            "equal": True,
            "legacy_output": legacy_output,
            "migrated_output": migrated_output,
            "differences": []
        }

    differences: List[Dict[str, Any]] = []

    if isinstance(legacy_output, dict) and isinstance(migrated_output, dict):
        all_keys = sorted(
            set(legacy_output.keys()) |
            set(migrated_output.keys())
        )

        for key in all_keys:
            legacy_value = legacy_output.get(key)
            migrated_value = migrated_output.get(key)

            if legacy_value != migrated_value:
                differences.append({
                    "field": key,
                    "legacy_value": legacy_value,
                    "migrated_value": migrated_value
                })

    else:
        differences.append({
            "field": "output",
            "legacy_value": legacy_output,
            "migrated_value": migrated_output
        })

    return {
        "verdict": "FAIL",
        "equal": False,
        "legacy_output": legacy_output,
        "migrated_output": migrated_output,
        "differences": differences
    }