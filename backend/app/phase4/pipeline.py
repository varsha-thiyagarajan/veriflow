from typing import Any, Dict, List

from .claim_failure import analyze_claim_failure
from .divergence_detector import detect_divergence
from .reasoning_tracer import trace_reasoning_chain


def run_phase4(verification_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run Phase 4 failure localization.

    Expected input:

    {
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "...",
                "confidence": 0.45,
                "verdict": "UNSUPPORTED",
                "evidence": [...]
            }
        ],

        "test_results": [
            {
                "test_id": "T001",
                "passed": False,
                "legacy_output": {...},
                "migrated_output": {...}
            }
        ],

        "reasoning_chains": [
            {
                "claim_id": "C001",
                "steps": [...]
            }
        ]
    }
    """

    claims: List[Dict[str, Any]] = verification_result.get("claims", [])
    test_results: List[Dict[str, Any]] = verification_result.get(
        "test_results", []
    )
    reasoning_chains: List[Dict[str, Any]] = verification_result.get(
        "reasoning_chains", []
    )

    # 1. Analyze claim failures
    claim_failures = [
        analyze_claim_failure(claim)
        for claim in claims
    ]

    # 2. Analyze code/output divergences
    divergences = [
        detect_divergence(test)
        for test in test_results
    ]

    # 3. Trace reasoning chains
    reasoning_traces = [
        trace_reasoning_chain(
            chain.get("claim_id", "UNKNOWN"),
            chain.get("steps", []),
        )
        for chain in reasoning_chains
    ]

    return {
        "phase": 4,
        "claim_failures": claim_failures,
        "divergences": divergences,
        "reasoning_traces": reasoning_traces,
    }