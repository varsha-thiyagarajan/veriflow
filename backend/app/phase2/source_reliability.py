from datetime import date
from .source_metadata import SourceMetadata


def calculate_freshness(publication_date: str | None) -> float:
    if not publication_date:
        return 0.5

    published = date.fromisoformat(publication_date)
    days_since_publication = (date.today() - published).days

    return 1 / (1 + days_since_publication / 365)


def calculate_citation_score(citation_count: int) -> float:
    return min(1.0, citation_count / 10)


def calculate_source_reliability(source: SourceMetadata) -> float:
    freshness = calculate_freshness(source.publication_date)
    citation_score = calculate_citation_score(source.citation_count)

    reliability = (
        0.5 * source.authority_level
        + 0.3 * freshness
        + 0.2 * citation_score
    )

    return round(reliability, 3)