import re
from typing import List, Dict


def extract_claims(text: str) -> List[Dict[str, str]]:
    """
    Extract atomic claims from input text.

    Each sentence is initially treated as one claim.
    More advanced atomic-claim decomposition can be added later.
    """

    if not text or not text.strip():
        return []

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text.strip())

    # Split text into sentences.
    sentences = re.split(r"(?<=[.!?])\s+", text)

    claims = []

    for index, sentence in enumerate(sentences, start=1):
        sentence = sentence.strip()

        if not sentence:
            continue

        claim = {
            "claim_id": f"C{index:03d}",
            "sentence_id": f"S{index:03d}",
            "claim_text": sentence,
        }

        claims.append(claim)

    return claims