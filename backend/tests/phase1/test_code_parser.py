from app.phase1.code_parser import parse_code


def test_parse_function():
    source = """
def calculate_tax(amount):
    if amount > 1000:
        result = amount * 0.8
        return result

    return amount * 0.9
"""

    result = parse_code(source)

    assert len(result) == 1

    function = result[0]

    assert function["function"] == "calculate_tax"
    assert function["parameters"] == ["amount"]

    assert "amount > 1000" in function["conditions"]

    assert "result = amount * 0.8" in function["transformations"]

    assert "result" in function["returns"]
    assert "amount * 0.9" in function["returns"]


def test_parse_loop():
    source = """
def calculate_total(items):
    total = 0

    for item in items:
        total = total + item

    return total
"""

    result = parse_code(source)

    function = result[0]

    assert function["function"] == "calculate_total"
    assert len(function["loops"]) == 1
    assert "for item in items" in function["loops"][0]


def test_empty_code():
    assert parse_code("") == []


def test_invalid_code():
    invalid_source = """
def broken_function(
"""

    try:
        parse_code(invalid_source)
        assert False
    except ValueError:
        assert True