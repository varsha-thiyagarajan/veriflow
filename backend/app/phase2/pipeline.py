from .retriever import retrieve_evidence
from .source_reliability import calculate_source_reliability
from .source_metadata import SourceMetadata


def run_phase2(claims, evidence_sources):
    results = []

    for claim in claims:
        claim_id = claim["claim_id"]
        claim_text = claim["claim_text"]

        retrieved = retrieve_evidence(
            claim_text,
            evidence_sources
        )

        evidence_results = []

        for evidence in retrieved:
            source = next(
                (
                    s for s in evidence_sources
                    if s["source_id"] == evidence["source_id"]
                ),
                None
            )

            if source:
                metadata = SourceMetadata(
                    source_id=source["source_id"],
                    title=source["title"],
                    url=source.get("url"),
                    authority_level=source["authority_level"],
                    publication_date=source.get("publication_date"),
                    citation_count=source.get("citation_count", 0),
                    domain=source.get("domain", "")
                )

                reliability = calculate_source_reliability(metadata)

                evidence_results.append({
                    **evidence,
                    "reliability": reliability
                })

        results.append({
            "claim_id": claim_id,
            "claim_text": claim_text,
            "evidence": evidence_results
        })

    return results