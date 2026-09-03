from backend.app.phase5.pipeline import run_phase5


def test_phase5_pipeline():
    claims = [
        {
            "claim_id": "C001",
            "claim_text": "The system supports authentication.",
            "verdict": "GROUNDED",
            "evidence": [{"source_id": "DOC001"}],
        },
        {
            "claim_id": "C002",
            "claim_text": "The system is scalable.",
            "verdict": "UNSUPPORTED",
            "evidence": [],
        },
    ]

    test_results = [
        {
            "test_id": "T001",
            "passed": True,
        },
        {
            "test_id": "T002",
            "passed": False,
        },
    ]

    phase4_result = {
        "claim_failures": [
            {
                "claim_id": "C002",
                "reason": "NO_EVIDENCE",
            }
        ],
        "divergences": [
            {
                "test_id": "T002",
                "diverged": True,
                "divergent_fields": ["total"],
            }
        ],
        "reasoning_traces": [],
    }

    input_data = {
        "text": "The system supports authentication.",
        "version": "1.0",
    }

    configuration = {
        "nli_model": "deberta",
        "threshold": 0.85,
    }

    result = run_phase5(
        artifact_id="ART001",
        artifact_type="TEXT",
        input_data=input_data,
        claims=claims,
        test_results=test_results,
        phase4_result=phase4_result,
        configuration=configuration,
    )

    assert result["phase"] == 5
    assert result["artifact_id"] == "ART001"

    # Trust Index
    assert result["trust_index"]["trust_index"] == 0.5
    assert result["trust_index"]["decision"] == "REJECT_OR_REGENERATE"

    # Audit report
    assert (
        result["audit_report"]["artifact"]["artifact_id"]
        == "ART001"
    )

    assert (
        result["audit_report"]["claim_verification"]["total_claims"]
        == 2
    )

    assert (
        result["audit_report"]["equivalence_testing"]["total_tests"]
        == 2
    )

    assert len(
        result["audit_report"]["failure_localization"][
            "claim_failures"
        ]
    ) == 1

    assert len(
        result["audit_report"]["failure_localization"][
            "divergences"
        ]
    ) == 1

    # Replay
    assert result["replay_record"]["artifact_id"] == "ART001"
    assert result["replay_record"]["artifact_type"] == "TEXT"
    assert result["replay_record"]["configuration"] == configuration
    assert len(result["replay_record"]["input_hash"]) == 64


def test_phase5_pipeline_with_empty_results():
    result = run_phase5(
        artifact_id="ART002",
        artifact_type="TEXT",
        input_data={},
        claims=[],
        test_results=[],
        phase4_result={},
    )

    assert result["phase"] == 5
    assert result["artifact_id"] == "ART002"

    assert result["trust_index"]["trust_index"] == 0.2
    assert (
        result["trust_index"]["decision"]
        == "REJECT_OR_REGENERATE"
    )

    assert (
        result["audit_report"]["claim_verification"]["total_claims"]
        == 0
    )

    assert (
        result["audit_report"]["equivalence_testing"]["total_tests"]
        == 0
    )

    assert result["replay_record"]["artifact_id"] == "ART002"
    assert result["replay_record"]["configuration"] == {}
    