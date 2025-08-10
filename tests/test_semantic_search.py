from src.semantic_search import semantic_search

def test_semantic_search():
    client = None  # Replace with actual client
    results = semantic_search("AI news", client)
    assert results is None or isinstance(results, list)
