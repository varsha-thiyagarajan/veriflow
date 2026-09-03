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


def get_domain_authority(domain: str) -> float:
    """
    Assign an authority score based on the source domain.

    1.0 = official / primary source
    0.7 = strong secondary / vendor documentation
    0.4 = community / general technical source
    0.2 = unattributed / unknown
    """

    domain = (domain or "").lower()

    official_domains = [
        "docs.oracle.com",
        "oracle.com",
        "docs.python.org",
        "python.org",
        "docs.microsoft.com",
        "learn.microsoft.com",
        "developer.mozilla.org",
        "java.com",
        "openjdk.org",
    ]

    secondary_domains = [
        "geeksforgeeks.org",
        "baeldung.com",
        "w3schools.com",
    ]

    community_domains = [
        "stackoverflow.com",
        "coderanch.com",
        "medium.com",
        "dev.to",
        "reddit.com",
    ]

    if any(
        domain == item or domain.endswith("." + item)
        for item in official_domains
    ):
        return 1.0

    if any(
        domain == item or domain.endswith("." + item)
        for item in secondary_domains
    ):
        return 0.7

    if any(
        domain == item or domain.endswith("." + item)
        for item in community_domains
    ):
        return 0.4

    return 0.2


def calculate_source_reliability(source: SourceMetadata) -> float:
    authority = source.authority_level

    if authority <= 0:
        authority = get_domain_authority(source.domain)

    freshness = calculate_freshness(source.publication_date)
    citation_score = calculate_citation_score(source.citation_count)

    reliability = (
        0.5 * authority
        + 0.3 * freshness
        + 0.2 * citation_score
    )

    return round(reliability, 3)