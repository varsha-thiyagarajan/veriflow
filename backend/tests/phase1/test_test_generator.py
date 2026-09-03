from app.phase1.test_generator import (
    extract_numeric_threshold,
    generate_boundary_values,
    generate_test_cases,
)


def test_extract_numeric_threshold():
    assert extract_numeric_threshold("amount > 1000") == 1000
    assert extract_numeric_threshold("score >= 500") == 500
    assert extract_numeric_threshold("value < 50") == 50


def test_extract_numeric_threshold_without_number():
    assert extract_numeric_threshold("amount > limit") is None


def test_generate_boundary_values():
    assert generate_boundary_values(1000) == [999, 1000, 1001]
    assert generate_boundary_values(50.0) == [49, 50, 51]


def test_generate_tests_for_function_with_condition():
    code_units = [
        {
            "function": "calculate_tax",
            "parameters": ["amount"],
            "conditions": ["amount > 1000"],
            "loops": [],
            "returns": [
                "amount * 0.8",
                "amount * 0.9",
            ],
            "transformations": [],
        }
    ]

    tests = generate_test_cases(code_units)

    assert len(tests) == 5

    assert tests[0]["test_id"] == "T001"
    assert tests[0]["function"] == "calculate_tax"
    assert tests[0]["input"] == {"amount": 0}

    assert tests[1]["input"] == {"amount": 1}

    assert tests[2]["input"] == {"amount": 999}
    assert tests[2]["reason"] == "condition_boundary"

    assert tests[3]["input"] == {"amount": 1000}

    assert tests[4]["input"] == {"amount": 1001}


def test_generate_tests_for_different_threshold():
    code_units = [
        {
            "function": "check_score",
            "parameters": ["score"],
            "conditions": ["score >= 50"],
            "loops": [],
            "returns": ["True", "False"],
            "transformations": [],
        }
    ]

    tests = generate_test_cases(code_units)

    assert tests[2]["input"] == {"score": 49}
    assert tests[3]["input"] == {"score": 50}
    assert tests[4]["input"] == {"score": 51}


def test_generate_tests_without_parameters():
    code_units = [
        {
            "function": "get_status",
            "parameters": [],
            "conditions": [],
            "loops": [],
            "returns": ["OK"],
            "transformations": [],
        }
    ]

    tests = generate_test_cases(code_units)

    assert tests == []


def test_empty_code_units():
    assert generate_test_cases([]) == []