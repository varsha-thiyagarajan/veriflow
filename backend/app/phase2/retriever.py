from typing import List, Dict


def retrieve_evidence(
    claim_text: str,
    evidence_sources: List[Dict]
) -> List[Dict]:
    """
    Retrieve evidence that is relevant to the given claim.
    """

    claim_words = set(claim_text.lower().split())

    results = []

    for source in evidence_sources:
        evidence_text = source.get("text", "")
        evidence_words = set(evidence_text.lower().split())

        overlap = claim_words.intersection(evidence_words)

        if overlap:
            results.append({
                "source_id": source.get("source_id"),
                "title": source.get("title"),
                "text": evidence_text,
                "matched_words": list(overlap)
            })

    return results