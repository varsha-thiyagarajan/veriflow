from typing import Any, Dict, List

from .web_search import search_web_with_content


def retrieve_evidence(
    claim_text: str,
    evidence_sources: List[Dict[str, Any]] | None = None,
    use_web: bool = False,
) -> List[Dict[str, Any]]:
    """
    Retrieve evidence for a claim.

    Local evidence can be used for deterministic testing.
    External web retrieval is enabled explicitly with use_web=True.
    """

    results = []

    # Local evidence path
    if evidence_sources:
        claim_words = set(claim_text.lower().split())

        for source in evidence_sources:
            evidence_text = source.get("text", "")
            evidence_words = set(evidence_text.lower().split())

            overlap = claim_words.intersection(evidence_words)

            if overlap:
                results.append({
                    "source_id": source.get("source_id"),
                    "title": source.get("title"),
                    "url": source.get("url"),
                    "text": evidence_text,
                    "matched_words": list(overlap),
                })

    # External web path
    if use_web:
        web_results = search_web_with_content(
            query=claim_text,
            num_results=5,
        )

        for index, source in enumerate(web_results, start=1):
            results.append({
                "source_id": f"WEB-{index:03d}",
                "title": source["title"],
                "url": source["url"],
                "text": source["text"],
                "snippet": source["snippet"],
                "matched_words": [],
            })

    return results