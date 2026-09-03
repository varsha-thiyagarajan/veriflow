from typing import Any, Dict, List

from .audit_report import generate_audit_report
from .replay import create_replay_record
from .trust_index import calculate_trust_index_from_results


def run_phase5(
    artifact_id: str,
    artifact_type: str,
    input_data: Dict[str, Any],
    claims: List[Dict[str, Any]],
    test_results: List[Dict[str, Any]],
    phase4_result: Dict[str, Any],
    configuration: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Run the complete Phase 5 audit and reproducibility pipeline.

    Phase 5 performs three main tasks:

    1. Calculate the Trust Index.
    2. Generate the complete audit report.
    3. Create a replay record for reproducibility.
    """

    # 1. Calculate Trust Index
    trust_index_result = calculate_trust_index_from_results(
        claims,
        test_results,
    )

    # 2. Generate Audit Report
    audit_report = generate_audit_report(
        artifact_id=artifact_id,
        artifact_type=artifact_type,
        claims=claims,
        test_results=test_results,
        phase4_result=phase4_result,
        trust_index_result=trust_index_result,
    )

    # 3. Create Replay Record
    replay_record = create_replay_record(
        artifact_id=artifact_id,
        artifact_type=artifact_type,
        input_data=input_data,
        configuration=configuration,
    )

    return {
        "phase": 5,
        "artifact_id": artifact_id,
        "trust_index": trust_index_result,
        "audit_report": audit_report,
        "replay_record": replay_record,
    }