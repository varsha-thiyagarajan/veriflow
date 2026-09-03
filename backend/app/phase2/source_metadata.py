from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceMetadata:
    source_id: str
    title: str
    url: Optional[str]
    authority_level: float
    publication_date: Optional[str]
    citation_count: int
    domain: str