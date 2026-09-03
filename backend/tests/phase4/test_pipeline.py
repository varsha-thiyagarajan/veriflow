from backend.app.phase4.pipeline import run_phase4


def test_phase4_pipeline():
    result = run_phase4({
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "The system supports authentication.",
                "confidence": 0.40,
                "verdict": "UNSUPPORTED",
                "evidence": []
            }
        ],
        "test_results": [
            {
                "test_id": "T001",
                "passed": False,
                "legacy_output": {
                    "total": 100
                },
                "migrated_output": {
                    "total": 120
                }
            }
        ],
        "reasoning_chains": [
            {
                "claim_id": "C001",
                "steps": [
                    {
                        "step_id": "S1",
                        "text": "Authentication is enabled.",
                        "supported": False,
                        "confidence": 0.30
                    }
                ]
            }
        ]
    })

    assert result["phase"] == 4

    assert len(result["claim_failures"]) == 1
    assert result["claim_failures"][0]["reason"] == "NO_EVIDENCE"

    assert len(result["divergences"]) == 1
    assert result["divergences"][0]["diverged"] is True
    assert result["divergences"][0]["divergent_fields"] == ["total"]

    assert len(result["reasoning_traces"]) == 1
    assert (
        result["reasoning_traces"][0]["reason"]
        == "UNSUPPORTED_REASONING_STEP"
    )
    assert (
        result["reasoning_traces"][0]["weakest_step"]["step_id"]
        == "S1"
    )


def test_phase4_pipeline_with_empty_input():
    result = run_phase4({
        "claims": [],
        "test_results": [],
        "reasoning_chains": []
    })

    assert result["phase"] == 4
    assert result["claim_failures"] == []
    assert result["divergences"] == []
    assert result["reasoning_traces"] == []