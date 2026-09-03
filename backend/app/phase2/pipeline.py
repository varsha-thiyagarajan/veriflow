from .retriever import retrieve_evidence
from .source_reliability import calculate_source_reliability
from .source_metadata import SourceMetadata


def run_phase2(
    claims,
    evidence_sources=None,
    use_web=True,
):
    """
    Run Phase 2 evidence retrieval.

    Claims come from Phase 1.
    Evidence can come from external web search
    and/or local sources.
    """

    results = []

    for claim in claims:
        claim_id = claim["claim_id"]
        claim_text = claim["claim_text"]

        retrieved = retrieve_evidence(
            claim_text=claim_text,
            evidence_sources=evidence_sources,
            use_web=use_web,
        )

        evidence_results = []

        for evidence in retrieved:

            # Web results receive a reasonable baseline authority.
            # Local sources can provide their own metadata.
            if evidence_sources:
                source = next(
                    (
                        s for s in evidence_sources
                        if s["source_id"] == evidence["source_id"]
                    ),
                    None
                )
            else:
                source = None

            if source:
                metadata = SourceMetadata(
                    source_id=source["source_id"],
                    title=source["title"],
                    url=source.get("url"),
                    authority_level=source["authority_level"],
                    publication_date=source.get("publication_date"),
                    citation_count=source.get("citation_count", 0),
                    domain=source.get("domain", ""),
                )
            else:
                metadata = SourceMetadata(
                    source_id=evidence["source_id"],
                    title=evidence["title"],
                    url=evidence.get("url"),
                    authority_level=0.5,
                    publication_date=None,
                    citation_count=0,
                    domain="web",
                )

            reliability = calculate_source_reliability(metadata)

            evidence_results.append({
                **evidence,
                "reliability": reliability,
            })

        results.append({
            "claim_id": claim_id,
            "claim_text": claim_text,
            "evidence": evidence_results,
        })

    return results