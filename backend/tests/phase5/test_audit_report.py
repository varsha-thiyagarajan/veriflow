from backend.app.phase5.audit_report import (
    generate_audit_report,
    summarize_audit_report,
)


def test_generate_audit_report():
    claims = [
        {
            "claim_id": "C001",
            "claim_text": "The system supports authentication.",
            "verdict": "GROUNDED",
            "confidence": 0.92,
            "evidence": [
                {"source_id": "DOC001"}
            ],
        },
        {
            "claim_id": "C002",
            "claim_text": "The system is scalable.",
            "verdict": "UNSUPPORTED",
            "confidence": 0.40,
            "evidence": [],
        },
    ]

    tests = [
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

    trust_index_result = {
        "trust_index": 0.76,
        "trust_index_percent": 76.0,
        "decision": "HUMAN_REVIEW",
    }

    report = generate_audit_report(
        artifact_id="ART001",
        artifact_type="TEXT",
        claims=claims,
        test_results=tests,
        phase4_result=phase4_result,
        trust_index_result=trust_index_result,
    )

    assert report["report_version"] == "1.0"

    assert "generated_at" in report

    assert report["artifact"]["artifact_id"] == "ART001"
    assert report["artifact"]["artifact_type"] == "TEXT"

    assert report["claim_verification"]["total_claims"] == 2
    assert len(report["claim_verification"]["claims"]) == 2

    assert report["equivalence_testing"]["total_tests"] == 2
    assert len(report["equivalence_testing"]["tests"]) == 2

    assert len(
        report["failure_localization"]["claim_failures"]
    ) == 1

    assert len(
        report["failure_localization"]["divergences"]
    ) == 1

    assert report["trust_index"]["trust_index"] == 0.76


def test_summarize_audit_report():
    report = generate_audit_report(
        artifact_id="ART002",
        artifact_type="CODE",
        claims=[
            {
                "claim_id": "C001",
                "verdict": "GROUNDED",
                "evidence": [{"source_id": "DOC001"}],
            },
            {
                "claim_id": "C002",
                "verdict": "GROUNDED",
                "evidence": [{"source_id": "DOC002"}],
            },
            {
                "claim_id": "C003",
                "verdict": "UNSUPPORTED",
                "evidence": [],
            },
        ],
        test_results=[
            {"test_id": "T001", "passed": True},
            {"test_id": "T002", "passed": False},
        ],
        phase4_result={
            "claim_failures": [
                {
                    "claim_id": "C003",
                    "reason": "NO_EVIDENCE",
                }
            ],
            "divergences": [
                {
                    "test_id": "T002",
                    "diverged": True,
                }
            ],
            "reasoning_traces": [
                {
                    "claim_id": "C003",
                    "weakest_step": {
                        "step_id": "S1"
                    },
                }
            ],
        },
        trust_index_result={
            "trust_index": 0.75,
            "decision": "HUMAN_REVIEW",
        },
    )

    summary = summarize_audit_report(report)

    assert summary["artifact_id"] == "ART002"
    assert summary["total_claims"] == 3
    assert summary["grounded_claims"] == 2

    assert summary["total_tests"] == 2
    assert summary["passed_tests"] == 1

    assert summary["claim_failures"] == 1
    assert summary["divergences"] == 1
    assert summary["reasoning_issues"] == 1

    assert summary["trust_index"] == 0.75
    assert summary["decision"] == "HUMAN_REVIEW"


def test_empty_audit_report():
    report = generate_audit_report(
        artifact_id="ART003",
        artifact_type="TEXT",
        claims=[],
        test_results=[],
        phase4_result={},
        trust_index_result={},
    )

    assert report["artifact"]["artifact_id"] == "ART003"
    assert report["claim_verification"]["total_claims"] == 0
    assert report["equivalence_testing"]["total_tests"] == 0
    assert report["failure_localization"]["claim_failures"] == []
    assert report["failure_localization"]["divergences"] == []
    assert report["failure_localization"]["reasoning_traces"] == []


def test_summary_with_no_failures():
    report = generate_audit_report(
        artifact_id="ART004",
        artifact_type="CODE",
        claims=[
            {
                "claim_id": "C001",
                "verdict": "GROUNDED",
                "evidence": [{"source_id": "DOC001"}],
            }
        ],
        test_results=[
            {
                "test_id": "T001",
                "passed": True,
            }
        ],
        phase4_result={
            "claim_failures": [],
            "divergences": [],
            "reasoning_traces": [],
        },
        trust_index_result={
            "trust_index": 0.95,
            "decision": "PRODUCTION_READY",
        },
    )

    summary = summarize_audit_report(report)

    assert summary["grounded_claims"] == 1
    assert summary["passed_tests"] == 1
    assert summary["claim_failures"] == 0
    assert summary["divergences"] == 0
    assert summary["reasoning_issues"] == 0
    assert summary["trust_index"] == 0.95
    assert summary["decision"] == "PRODUCTION_READY"