import pytest

from app.phase1.pipeline import (
    process_artefact,
    process_code,
    process_text,
)


def test_text_pipeline():
    text = (
        "The system validates user input. "
        "Therefore, invalid requests are rejected. "
        "The system must log rejected requests."
    )

    result = process_text(text)

    assert result["input_type"] == "text"
    assert len(result["claims"]) == 3

    assert result["claims"][0]["claim_type"] == "FACTUAL"
    assert result["claims"][1]["claim_type"] == "INFERENTIAL"
    assert result["claims"][2]["claim_type"] == "NORMATIVE"

    assert result["code_units"] == []
    assert result["tests"] == []


def test_empty_text_pipeline():
    result = process_text("")

    assert result["input_type"] == "text"
    assert result["claims"] == []
    assert result["code_units"] == []
    assert result["tests"] == []


def test_code_pipeline():
    source = """
def calculate_tax(amount):
    if amount > 1000:
        result = amount * 0.8
        return result

    return amount * 0.9
"""

    result = process_code(source)

    assert result["input_type"] == "code"

    assert result["claims"] == []

    assert len(result["code_units"]) == 1

    function = result["code_units"][0]

    assert function["function"] == "calculate_tax"
    assert function["parameters"] == ["amount"]
    assert "amount > 1000" in function["conditions"]

    assert len(result["tests"]) == 5

    assert result["tests"][0]["input"] == {"amount": 0}
    assert result["tests"][1]["input"] == {"amount": 1}
    assert result["tests"][2]["input"] == {"amount": 999}
    assert result["tests"][3]["input"] == {"amount": 1000}
    assert result["tests"][4]["input"] == {"amount": 1001}


def test_main_artefact_router_for_text():
    result = process_artefact(
        "text",
        "The application validates input.",
    )

    assert result["input_type"] == "text"
    assert len(result["claims"]) == 1


def test_main_artefact_router_for_code():
    source = """
def add(a, b):
    return a + b
"""

    result = process_artefact("code", source)

    assert result["input_type"] == "code"
    assert result["code_units"][0]["function"] == "add"


def test_invalid_input_type():
    with pytest.raises(ValueError):
        process_artefact("image", "some content")