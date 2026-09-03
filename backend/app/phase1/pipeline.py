from typing import Any, Dict

from app.phase1.claim_classifier import classify_claim_object
from app.phase1.claim_extractor import extract_claims
from app.phase1.code_parser import parse_code
from app.phase1.test_generator import generate_test_cases


def process_text(text: str) -> Dict[str, Any]:
    """
    Process a text artefact.

    Steps:
    1. Extract claims.
    2. Classify each claim.
    3. Return structured Phase 1 output.
    """

    extracted_claims = extract_claims(text)

    classified_claims = [
        classify_claim_object(claim)
        for claim in extracted_claims
    ]

    return {
        "input_type": "text",
        "claims": classified_claims,
        "code_units": [],
        "tests": [],
    }


def process_code(source_code: str) -> Dict[str, Any]:
    """
    Process a Python code artefact.

    Steps:
    1. Parse Python source using AST.
    2. Extract functions, parameters, conditions,
       loops, returns, and transformations.
    3. Generate characterization test cases.
    """

    code_units = parse_code(source_code)

    tests = generate_test_cases(code_units)

    return {
        "input_type": "code",
        "claims": [],
        "code_units": code_units,
        "tests": tests,
    }


def process_artefact(
    input_type: str,
    content: str,
) -> Dict[str, Any]:
    """
    Main Phase 1 entry point.

    input_type must be either 'text' or 'code'.
    """

    if input_type == "text":
        return process_text(content)

    if input_type == "code":
        return process_code(content)

    raise ValueError(
        "input_type must be either 'text' or 'code'."
    )