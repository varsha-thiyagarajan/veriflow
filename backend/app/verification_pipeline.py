from typing import Any, Dict

from app.phase1.pipeline import process_artefact
from app.phase2.pipeline import run_phase2
from app.phase3.pipeline import run_text_verification


def run_text_verification_pipeline(
    content: str,
) -> Dict[str, Any]:
    """
    Run the complete text verification flow:

    Phase 1:
        Extract and classify claims.

    Phase 2:
        Retrieve evidence from the external web.

    Phase 3:
        Verify claims with NLI and consensus.
    """

    # Phase 1
    phase1_result = process_artefact(
        input_type="text",
        content=content,
    )

    claims = phase1_result["claims"]

    # Phase 2
    phase2_result = run_phase2(
        claims=claims,
        evidence_sources=None,
        use_web=True,
    )

    # Phase 3
    phase3_result = run_text_verification(
        phase2_result,
    )

    return {
        "input_type": "text",
        "original_content": content,
        "phase1": phase1_result,
        "phase2": phase2_result,
        "phase3": phase3_result,
    }