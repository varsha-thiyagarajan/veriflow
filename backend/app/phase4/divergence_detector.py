from typing import Any, Dict, List


def detect_divergence(test_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare legacy and migrated outputs for a single test.

    Expected input:
    {
        "test_id": "T001",
        "passed": False,
        "legacy_output": {
            "total": 100,
            "tax": 18
        },
        "migrated_output": {
            "total": 100,
            "tax": 20
        }
    }
    """

    test_id = test_result.get("test_id", "UNKNOWN")
    legacy_output = test_result.get("legacy_output")
    migrated_output = test_result.get("migrated_output")

    # Missing outputs cannot be compared.
    if legacy_output is None or migrated_output is None:
        return {
            "test_id": test_id,
            "diverged": True,
            "reason": "MISSING_OUTPUT",
            "divergent_fields": [],
        }

    # If both outputs are dictionaries, compare their fields.
    if isinstance(legacy_output, dict) and isinstance(migrated_output, dict):
        divergent_fields: List[str] = []

        all_fields = set(legacy_output.keys()) | set(migrated_output.keys())

        for field in all_fields:
            legacy_value = legacy_output.get(field)
            migrated_value = migrated_output.get(field)

            if legacy_value != migrated_value:
                divergent_fields.append(field)

        divergent_fields.sort()

        if divergent_fields:
            differences = {}

            for field in divergent_fields:
                differences[field] = {
                    "legacy": legacy_output.get(field),
                    "migrated": migrated_output.get(field),
                }

            return {
                "test_id": test_id,
                "diverged": True,
                "reason": "OUTPUT_MISMATCH",
                "divergent_fields": divergent_fields,
                "differences": differences,
            }

        return {
            "test_id": test_id,
            "diverged": False,
            "reason": None,
            "divergent_fields": [],
            "differences": {},
        }

    # For non-dictionary outputs, compare the complete values.
    if legacy_output != migrated_output:
        return {
            "test_id": test_id,
            "diverged": True,
            "reason": "OUTPUT_MISMATCH",
            "divergent_fields": ["output"],
            "differences": {
                "output": {
                    "legacy": legacy_output,
                    "migrated": migrated_output,
                }
            },
        }

    return {
        "test_id": test_id,
        "diverged": False,
        "reason": None,
        "divergent_fields": [],
        "differences": {},
    }