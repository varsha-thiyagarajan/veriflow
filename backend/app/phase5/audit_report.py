from datetime import datetime, timezone
from typing import Any, Dict, List


def generate_audit_report(
    artifact_id: str,
    artifact_type: str,
    claims: List[Dict[str, Any]],
    test_results: List[Dict[str, Any]],
    phase4_result: Dict[str, Any],
    trust_index_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a complete VeriFlow audit report.

    The report keeps the results from Phases 3, 4, and 5
    together so the verification process can be reviewed later.
    """

    return {
        "report_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifact": {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
        },
        "claim_verification": {
            "total_claims": len(claims),
            "claims": claims,
        },
        "equivalence_testing": {
            "total_tests": len(test_results),
            "tests": test_results,
        },
        "failure_localization": {
            "claim_failures": phase4_result.get(
                "claim_failures", []
            ),
            "divergences": phase4_result.get(
                "divergences", []
            ),
            "reasoning_traces": phase4_result.get(
                "reasoning_traces", []
            ),
        },
        "trust_index": trust_index_result,
    }


def summarize_audit_report(
    report: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create a compact summary of an audit report.
    """

    claims = report.get("claim_verification", {})
    tests = report.get("equivalence_testing", {})
    failures = report.get("failure_localization", {})
    trust = report.get("trust_index", {})

    claim_list = claims.get("claims", [])
    test_list = tests.get("tests", [])

    grounded_claims = sum(
        1
        for claim in claim_list
        if str(claim.get("verdict", "")).upper() == "GROUNDED"
    )

    passed_tests = sum(
        1
        for test in test_list
        if bool(test.get("passed", False))
    )

    return {
        "artifact_id": report.get("artifact", {}).get(
            "artifact_id"
        ),
        "total_claims": claims.get("total_claims", 0),
        "grounded_claims": grounded_claims,
        "total_tests": tests.get("total_tests", 0),
        "passed_tests": passed_tests,
        "claim_failures": len(
            failures.get("claim_failures", [])
        ),
        "divergences": len(
            failures.get("divergences", [])
        ),
        "reasoning_issues": sum(
            1
            for trace in failures.get("reasoning_traces", [])
            if trace.get("weakest_step") is not None
        ),
        "trust_index": trust.get("trust_index"),
        "decision": trust.get("decision"),
    }