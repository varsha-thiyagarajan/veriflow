from backend.app.phase4.reasoning_tracer import trace_reasoning_chain


def test_no_reasoning_steps():
    result = trace_reasoning_chain("C001", [])

    assert result["reason"] == "NO_REASONING_STEPS"
    assert result["weakest_step"] is None


def test_unsupported_step_is_weakest():
    result = trace_reasoning_chain(
        "C002",
        [
            {
                "step_id": "S1",
                "text": "Revenue increased.",
                "supported": True,
                "confidence": 0.95,
            },
            {
                "step_id": "S2",
                "text": "Costs decreased.",
                "supported": False,
                "confidence": 0.35,
            },
        ],
    )

    assert result["reason"] == "UNSUPPORTED_REASONING_STEP"
    assert result["weakest_step"]["step_id"] == "S2"


def test_low_confidence_step():
    result = trace_reasoning_chain(
        "C003",
        [
            {
                "step_id": "S1",
                "text": "Revenue increased.",
                "supported": True,
                "confidence": 0.95,
            },
            {
                "step_id": "S2",
                "text": "Profit increased.",
                "supported": True,
                "confidence": 0.50,
            },
        ],
    )

    assert result["reason"] == "LOW_CONFIDENCE_REASONING_STEP"
    assert result["weakest_step"]["step_id"] == "S2"


def test_all_steps_supported():
    result = trace_reasoning_chain(
        "C004",
        [
            {
                "step_id": "S1",
                "text": "Revenue increased.",
                "supported": True,
                "confidence": 0.95,
            },
            {
                "step_id": "S2",
                "text": "Costs decreased.",
                "supported": True,
                "confidence": 0.90,
            },
        ],
    )

    assert result["reason"] == "NO_WEAK_STEP"
    assert result["weakest_step"] is None


def test_multiple_unsupported_steps():
    result = trace_reasoning_chain(
        "C005",
        [
            {
                "step_id": "S1",
                "text": "Revenue increased.",
                "supported": False,
                "confidence": 0.40,
            },
            {
                "step_id": "S2",
                "text": "Costs decreased.",
                "supported": False,
                "confidence": 0.20,
            },
        ],
    )

    assert result["reason"] == "UNSUPPORTED_REASONING_STEP"
    assert result["weakest_step"]["step_id"] == "S2"


def test_step_statuses():
    result = trace_reasoning_chain(
        "C006",
        [
            {
                "step_id": "S1",
                "text": "Supported fact.",
                "supported": True,
                "confidence": 0.90,
            },
            {
                "step_id": "S2",
                "text": "Weak fact.",
                "supported": True,
                "confidence": 0.50,
            },
            {
                "step_id": "S3",
                "text": "Unsupported fact.",
                "supported": False,
                "confidence": 0.30,
            },
        ],
    )

    statuses = {
        step["step_id"]: step["status"]
        for step in result["steps"]
    }

    assert statuses["S1"] == "SUPPORTED"
    assert statuses["S2"] == "LOW_CONFIDENCE"
    assert statuses["S3"] == "UNSUPPORTED"