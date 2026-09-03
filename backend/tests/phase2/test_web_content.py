from app.phase2.web_search import search_web_with_content


def test_web_search_with_page_content():
    results = search_web_with_content(
        "Java HashMap null keys",
        num_results=3,
    )

    assert len(results) > 0

    first = results[0]

    assert first["title"]
    assert first["url"]
    assert first["snippet"]
    assert first["text"]