import pytest
from src.scraper import extract_article

@pytest.mark.asyncio
async def test_extract_article():
    url = "https://example.com/news"
    result = await extract_article(url)
    assert hasattr(result, "headline") and hasattr(result, "text")
