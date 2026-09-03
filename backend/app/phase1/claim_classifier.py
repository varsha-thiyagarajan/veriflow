from typing import Dict


FACTUAL = "FACTUAL"
INFERENTIAL = "INFERENTIAL"
NORMATIVE = "NORMATIVE"


def classify_claim(claim_text: str) -> str:
    """
    Classify a claim into:
    - FACTUAL
    - INFERENTIAL
    - NORMATIVE

    This is a lightweight rule-based baseline.
    It can later be replaced or enhanced with an LLM/model.
    """

    text = claim_text.strip().lower()

    if not text:
        raise ValueError("Claim text cannot be empty.")

    # Normative claims express recommendations,
    # requirements, obligations, or judgments.
    normative_patterns = [
        "should ",
        "must ",
        "ought to ",
        "recommended",
        "required",
        "better to ",
        "need to ",
    ]

    for pattern in normative_patterns:
        if pattern in text:
            return NORMATIVE

    # Inferential claims indicate conclusions,
    # causes, implications, or reasoning.
    inferential_patterns = [
        "therefore",
        "thus",
        "hence",
        "because",
        "implies",
        "suggests",
        "indicates",
        "as a result",
        "likely",
        "probably",
    ]

    for pattern in inferential_patterns:
        if pattern in text:
            return INFERENTIAL

    # Default category.
    return FACTUAL


def classify_claim_object(claim: Dict[str, str]) -> Dict[str, str]:
    """
    Add claim_type to an extracted claim object.
    """

    if "claim_text" not in claim:
        raise ValueError("Claim object must contain 'claim_text'.")

    result = claim.copy()
    result["claim_type"] = classify_claim(claim["claim_text"])

    return result