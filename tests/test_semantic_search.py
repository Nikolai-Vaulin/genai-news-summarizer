import pytest
from src.semantic_search import semantic_search

@pytest.mark.asyncio
async def test_semantic_search():
    client = None  # Replace with actual client or mock
    results = await semantic_search("AI news", client)
    assert results is None or isinstance(results, list)
