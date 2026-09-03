from app.phase2.retriever import retrieve_evidence
from app.phase2.source_reliability import (
    calculate_citation_score,
    calculate_freshness,
    calculate_source_reliability,
)
from app.phase2.source_metadata import SourceMetadata
from app.phase2.pipeline import run_phase2


def test_retriever_finds_matching_evidence():
    claim = "HashMap allows null keys"

    sources = [
        {
            "source_id": "S001",
            "title": "Java Documentation",
            "text": "HashMap allows null keys and values."
        }
    ]

    result = retrieve_evidence(claim, sources)

    assert len(result) == 1
    assert result[0]["source_id"] == "S001"


def test_retriever_returns_empty_for_no_match():
    claim = "Java uses garbage collection"

    sources = [
        {
            "source_id": "S001",
            "title": "Java Documentation",
            "text": "HashMap allows null keys and values."
        }
    ]

    result = retrieve_evidence(claim, sources)

    assert result == []


def test_citation_score():
    assert calculate_citation_score(5) == 0.5
    assert calculate_citation_score(10) == 1.0
    assert calculate_citation_score(20) == 1.0


def test_freshness_without_date():
    assert calculate_freshness(None) == 0.5


def test_source_reliability():
    source = SourceMetadata(
        source_id="S001",
        title="Java Documentation",
        url="https://example.com",
        authority_level=1.0,
        publication_date=None,
        citation_count=10,
        domain="java"
    )

    reliability = calculate_source_reliability(source)

    assert reliability == 0.85


def test_phase2_pipeline():
    claims = [
        {
            "claim_id": "C001",
            "claim_text": "HashMap allows null keys"
        }
    ]

    sources = [
        {
            "source_id": "S001",
            "title": "Java Documentation",
            "url": "https://example.com",
            "authority_level": 1.0,
            "publication_date": None,
            "citation_count": 10,
            "domain": "java",
            "text": "HashMap allows null keys and values."
        }
    ]

    result = run_phase2(claims, sources)

    assert len(result) == 1
    assert result[0]["claim_id"] == "C001"
    assert len(result[0]["evidence"]) == 1
    assert result[0]["evidence"][0]["reliability"] == 0.85