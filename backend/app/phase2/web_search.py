from .source_reliability import get_domain_authority
import os
import re
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"


def search_web(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web using Serper and return normalized results.
    """

    if not SERPER_API_KEY:
        raise RuntimeError("SERPER_API_KEY is not configured.")

    response = requests.post(
        SERPER_URL,
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "q": query,
            "num": num_results,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("organic", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })

    return results


def fetch_page_text(url: str, timeout: int = 10) -> str:
    """
    Fetch readable text from a web page.
    """

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/128.0 Safari/537.36"
                )
            },
            timeout=timeout,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside",
        ]):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True,
        )

        return text[:12000]

    except requests.RequestException:
        return ""
    except Exception:
        return ""


def extract_relevant_passage(
    page_text: str,
    query: str,
    max_sentences: int = 3,
) -> str:
    """
    Select the most relevant sentences from a webpage
    for the current claim.
    """

    if not page_text:
        return ""

    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "to",
        "of",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "has",
        "have",
        "can",
        "be",
        "this",
        "that",
        "it",
        "as",
        "by",
        "from",
        "does",
    }

    query_words = {
        word
        for word in re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query.lower(),
        )
        if word not in stop_words
    }

    sentences = re.split(
        r"(?<=[.!?])\s+",
        page_text,
    )

    scored_sentences = []

    for sentence in sentences:
        sentence_words = {
            word
            for word in re.findall(
                r"\b[a-zA-Z0-9]+\b",
                sentence.lower(),
            )
            if word not in stop_words
        }

        overlap = query_words.intersection(sentence_words)

        if overlap:
            score = len(overlap)

            scored_sentences.append(
                (score, sentence.strip())
            )

    scored_sentences.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    selected = [
        sentence
        for _, sentence in scored_sentences[:max_sentences]
        if sentence
    ]

    return " ".join(selected)


def search_web_with_content(
    query: str,
    num_results: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search the web, enrich results with focused evidence,
    and prioritize higher-authority domains.
    """

    # Retrieve extra results so authoritative sources have
    # a better chance of entering the final evidence set.
    search_results = search_web(
        query=query,
        num_results=max(num_results, 10),
    )

    enriched_results = []

    for result in search_results:
        url = result.get("url", "")

        domain = ""
        if url:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.lower()

        authority = get_domain_authority(domain)

        page_text = fetch_page_text(url)

        if page_text:
            evidence_text = extract_relevant_passage(
                page_text=page_text,
                query=query,
                max_sentences=3,
            )
        else:
            evidence_text = result["snippet"]

        if not evidence_text:
            evidence_text = result["snippet"]

        enriched_results.append({
            "title": result["title"],
            "url": url,
            "domain": domain,
            "authority": authority,
            "snippet": result["snippet"],
            "text": evidence_text,
        })

    # Highest-authority sources first.
    enriched_results.sort(
        key=lambda item: item["authority"],
        reverse=True,
    )

    return enriched_results[:num_results]