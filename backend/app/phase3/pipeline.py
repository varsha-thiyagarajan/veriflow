from .nli_verifier import verify_claim
from .behavioral_tester import compare_outputs
from .consensus import (
    calculate_consensus_score,
    calculate_claim_confidence,
    get_claim_verdict,
)


def run_text_verification(claims_with_evidence):
    results = []

    for item in claims_with_evidence:
        claim_id = item["claim_id"]
        claim_text = item["claim_text"]
        evidence_items = item.get("evidence", [])

        if not evidence_items:
            results.append({
                "claim_id": claim_id,
                "claim_text": claim_text,
                "verdict": "UNSUPPORTED",
                "confidence": 0.0,
                "consensus_score": 0.0,
                "nli_results": [],
            })
            continue

        nli_results = []

        for evidence in evidence_items:
            nli = verify_claim(
                claim=claim_text,
                evidence=evidence["text"],
            )

            nli_results.append({
                **nli,
                "source_reliability": evidence.get("reliability", 0.0),
                "source_id": evidence.get("source_id"),
            })

        total_sources = len(nli_results)

        agreeing_sources = sum(
            1
            for result in nli_results
            if result["verdict"] == "entailment"
        )

        average_agreement_strength = sum(
            result["entailment_probability"]
            for result in nli_results
        ) / total_sources

        consensus_score = calculate_consensus_score(
            agreeing_sources,
            total_sources,
            average_agreement_strength,
        )

        average_reliability = sum(
            result["source_reliability"]
            for result in nli_results
        ) / total_sources

        best_nli = max(
            nli_results,
            key=lambda result: result["entailment_probability"],
        )

        confidence = calculate_claim_confidence(
            best_nli["entailment_probability"],
            average_reliability,
            consensus_score,
        )

        contradiction_probability = max(
            result["contradiction_probability"]
            for result in nli_results
        )

        verdict = get_claim_verdict(
            confidence,
            contradiction_probability,
        )

        results.append({
            "claim_id": claim_id,
            "claim_text": claim_text,
            "verdict": verdict,
            "confidence": confidence,
            "consensus_score": consensus_score,
            "nli_results": nli_results,
        })

    return results


def run_code_verification(test_cases):
    results = []

    for test in test_cases:
        comparison = compare_outputs(
            test["legacy_output"],
            test["migrated_output"],
        )

        results.append({
            "test_id": test["test_id"],
            **comparison,
        })

    total_tests = len(results)

    passed_tests = sum(
        1
        for result in results
        if result["verdict"] == "PASS"
    )

    pass_rate = (
        passed_tests / total_tests
        if total_tests
        else 0.0
    )

    return {
        "tests": results,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "pass_rate": round(pass_rate, 3),
        "verdict": (
            "PASS"
            if total_tests > 0 and passed_tests == total_tests
            else "FAIL"
        ),
    }