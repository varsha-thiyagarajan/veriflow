import re
from typing import Any, Dict, List, Optional


def extract_numeric_threshold(condition: str) -> Optional[float]:
    """
    Extract the first numeric threshold from a condition.

    Examples:
        'amount > 1000' -> 1000
        'score >= 500' -> 500
        'value < 50' -> 50
    """

    match = re.search(r"[-+]?\d+(?:\.\d+)?", condition)

    if not match:
        return None

    return float(match.group())


def generate_boundary_values(threshold: float) -> List[float | int]:
    """
    Generate representative values around a numeric threshold.

    For example:
        1000 -> [999, 1000, 1001]
        50.0 -> [49, 50, 51]
    """

    if threshold.is_integer():
        threshold = int(threshold)

    return [
        threshold - 1,
        threshold,
        threshold + 1,
    ]


def generate_test_cases(
    code_units: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate representative characterization test cases
    from parsed code units.

    The generated cases capture baseline and important
    condition-boundary behavior before migration.
    """

    test_cases: List[Dict[str, Any]] = []

    test_number = 1

    for function in code_units:
        function_name = function["function"]
        parameters = function.get("parameters", [])
        conditions = function.get("conditions", [])

        # Generate baseline tests.
        if parameters:
            zero_input = {
                parameter: 0
                for parameter in parameters
            }

            test_cases.append(
                {
                    "test_id": f"T{test_number:03d}",
                    "function": function_name,
                    "input": zero_input,
                    "reason": "baseline_zero_input",
                }
            )

            test_number += 1

            positive_input = {
                parameter: 1
                for parameter in parameters
            }

            test_cases.append(
                {
                    "test_id": f"T{test_number:03d}",
                    "function": function_name,
                    "input": positive_input,
                    "reason": "baseline_positive_input",
                }
            )

            test_number += 1

        # Generate tests around numeric condition thresholds.
        if conditions and parameters:
            for condition in conditions:
                threshold = extract_numeric_threshold(condition)

                if threshold is None:
                    continue

                boundary_values = generate_boundary_values(threshold)

                # Use the first parameter for simple single-parameter
                # boundary tests.
                parameter = parameters[0]

                for value in boundary_values:
                    test_cases.append(
                        {
                            "test_id": f"T{test_number:03d}",
                            "function": function_name,
                            "input": {
                                parameter: value
                            },
                            "reason": "condition_boundary",
                            "condition": condition,
                        }
                    )

                    test_number += 1

    return test_cases