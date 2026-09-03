import os
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

        # Remove elements that are usually not useful as evidence.
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

        # Prevent extremely large pages from entering NLI.
        return text[:12000]

    except requests.RequestException:
        return ""
    except Exception:
        return ""


def search_web_with_content(
    query: str,
    num_results: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search the web and enrich each result with page content.

    Falls back to the search snippet when the page cannot
    be fetched.
    """

    search_results = search_web(
        query=query,
        num_results=num_results,
    )

    enriched_results = []

    for result in search_results:
        page_text = fetch_page_text(result["url"])

        evidence_text = page_text or result["snippet"]

        enriched_results.append({
            "title": result["title"],
            "url": result["url"],
            "snippet": result["snippet"],
            "text": evidence_text,
        })

    return enriched_results