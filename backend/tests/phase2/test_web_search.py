from app.phase2.web_search import search_web


def test_web_search():
    results = search_web("Java HashMap null key", num_results=3)

    assert isinstance(results, list)
    assert len(results) > 0

    first = results[0]

    assert "title" in first
    assert "url" in first
    assert "snippet" in first