from typing import Any, Dict, List


def trace_reasoning_chain(
    claim_id: str,
    reasoning_steps: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Identify the weakest step in a multi-step reasoning chain.

    Expected input:
    [
        {
            "step_id": "S1",
            "text": "Revenue increased.",
            "supported": True,
            "confidence": 0.95
        },
        {
            "step_id": "S2",
            "text": "Costs decreased.",
            "supported": False,
            "confidence": 0.35
        }
    ]
    """

    if not reasoning_steps:
        return {
            "claim_id": claim_id,
            "steps": [],
            "weakest_step": None,
            "reason": "NO_REASONING_STEPS",
        }

    traced_steps = []

    for step in reasoning_steps:
        step_id = step.get("step_id", "UNKNOWN")
        text = step.get("text", "")
        supported = bool(step.get("supported", False))
        confidence = float(step.get("confidence", 0.0))

        if not supported:
            status = "UNSUPPORTED"
        elif confidence < 0.60:
            status = "LOW_CONFIDENCE"
        else:
            status = "SUPPORTED"

        traced_steps.append({
            "step_id": step_id,
            "text": text,
            "supported": supported,
            "confidence": confidence,
            "status": status,
        })

    # Prefer an unsupported step as the weakest point.
    unsupported_steps = [
        step for step in traced_steps
        if step["status"] == "UNSUPPORTED"
    ]

    if unsupported_steps:
        weakest_step = min(
            unsupported_steps,
            key=lambda step: step["confidence"]
        )

        return {
            "claim_id": claim_id,
            "steps": traced_steps,
            "weakest_step": weakest_step,
            "reason": "UNSUPPORTED_REASONING_STEP",
        }

    # Otherwise find the step with the lowest confidence.
    weakest_step = min(
        traced_steps,
        key=lambda step: step["confidence"]
    )

    if weakest_step["status"] == "LOW_CONFIDENCE":
        reason = "LOW_CONFIDENCE_REASONING_STEP"
    else:
        reason = "NO_WEAK_STEP"

    return {
        "claim_id": claim_id,
        "steps": traced_steps,
        "weakest_step": weakest_step if reason != "NO_WEAK_STEP" else None,
        "reason": reason,
    }