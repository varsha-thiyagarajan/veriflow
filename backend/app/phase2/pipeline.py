from urllib.parse import urlparse

from .retriever import retrieve_evidence
from .source_reliability import calculate_source_reliability
from .source_metadata import SourceMetadata


def run_phase2(claims, evidence_sources=None, use_web=False):
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
            source = None

            if evidence_sources:
                source = next(
                    (
                        item
                        for item in evidence_sources
                        if item["source_id"] == evidence["source_id"]
                    ),
                    None,
                )

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
                url = evidence.get("url", "")
                domain = urlparse(url).netloc.lower()

                metadata = SourceMetadata(
                    source_id=evidence["source_id"],
                    title=evidence["title"],
                    url=url,
                    authority_level=0.0,
                    publication_date=None,
                    citation_count=0,
                    domain=domain,
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