from typing import Any, Dict, List


LOW_RELIABILITY_THRESHOLD = 0.60
FAILURE_CONFIDENCE_THRESHOLD = 0.60


def analyze_claim_failure(verification_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a verification result and explain why a claim failed.

    Expected input:
    {
        "claim_id": "C001",
        "claim_text": "...",
        "confidence": 0.45,
        "verdict": "UNSUPPORTED",
        "evidence": [
            {
                "source_id": "DOC001",
                "source_reliability": 0.91,
                "nli_label": "contradiction",
                "nli_probability": 0.80
            }
        ]
    }
    """

    claim_id = verification_result.get("claim_id", "UNKNOWN")
    claim_text = verification_result.get("claim_text", "")
    confidence = float(verification_result.get("confidence", 0.0))
    verdict = str(verification_result.get("verdict", "")).upper()

    evidence: List[Dict[str, Any]] = verification_result.get("evidence", [])

    # Supported claims do not have a failure.
    if verdict == "GROUNDED" and confidence >= FAILURE_CONFIDENCE_THRESHOLD:
        return {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "failed": False,
            "reason": None,
            "message": "Claim is sufficiently grounded.",
        }

    # Failure 1: No evidence
    if not evidence:
        return {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "failed": True,
            "reason": "NO_EVIDENCE",
            "message": "No supporting evidence was found for this claim.",
        }

    # Failure 2: Contradicting evidence
    contradictions = [
        item
        for item in evidence
        if str(item.get("nli_label", "")).lower() == "contradiction"
    ]

    if contradictions:
        source_ids = [
            item.get("source_id")
            for item in contradictions
            if item.get("source_id")
        ]

        return {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "failed": True,
            "reason": "CONTRADICTION",
            "message": "Evidence contradicts the claim.",
            "contradicting_sources": source_ids,
        }

    # Failure 3: Low source reliability
    reliability_values = [
        float(item.get("source_reliability", 0.0))
        for item in evidence
        if item.get("source_reliability") is not None
    ]

    if reliability_values:
        average_reliability = sum(reliability_values) / len(reliability_values)

        if average_reliability < LOW_RELIABILITY_THRESHOLD:
            return {
                "claim_id": claim_id,
                "claim_text": claim_text,
                "failed": True,
                "reason": "LOW_SOURCE_RELIABILITY",
                "message": "Available evidence comes from low-reliability sources.",
                "average_source_reliability": round(
                    average_reliability, 3
                ),
            }

    # Failure 4: Consensus mismatch / insufficient agreement
    labels = [
        str(item.get("nli_label", "")).lower()
        for item in evidence
        if item.get("nli_label")
    ]

    if len(set(labels)) > 1:
        return {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "failed": True,
            "reason": "CONSENSUS_MISMATCH",
            "message": "Evidence sources do not agree on the claim.",
            "evidence_labels": labels,
        }

    # Generic failure
    return {
        "claim_id": claim_id,
        "claim_text": claim_text,
        "failed": True,
        "reason": "INSUFFICIENT_CONFIDENCE",
        "message": "The claim could not be verified with sufficient confidence.",
        "confidence": confidence,
        "verdict": verdict,
    }