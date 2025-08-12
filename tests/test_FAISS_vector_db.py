import pytest
from src.vector_dbs.FAISS_vector_db import LangChainFAISSVectorDB

@pytest.fixture
def db():
    db = LangChainFAISSVectorDB()
    articles = [
        "Apple releases new iPhone with improved camera.",
        "Microsoft announces new AI features for Office.",
        "Google updates search algorithm for better results.",
        "Tesla unveils new electric truck model.",
        "Amazon expands grocery delivery service.",
        "Russian officials crow about landing a summit between President Vladimir Putin and President Donald Trump."
    ]
    metas = [
        {"topics": "tech", "headline": "Apple iPhone", "url": "https://apple.com"},
        {"topics": "ai", "headline": "Microsoft AI", "url": "https://microsoft.com"},
        {"topics": "search", "headline": "Google Search", "url": "https://google.com"},
        {"topics": "auto", "headline": "Tesla Truck", "url": "https://tesla.com"},
        {"topics": "retail", "headline": "Amazon Grocery", "url": "https://amazon.com"},
        {"topics": "politics", "headline": "Putin Trump Summit", "url": "https://example.com"}
    ]
    for article, meta in zip(articles, metas):
        db.add(article, meta, meta["url"])  # Pass URL as id
    return db

@pytest.mark.asyncio
async def test_semantic_search_basic(db: LangChainFAISSVectorDB):
    # Query for a tech topic
    results = await db.search("iPhone", k=1)
    assert any("Apple" in r.metadata["headline"] for r, distance in results)
    # Query for AI
    results = await db.search("AI", k=1)
    assert any("Microsoft" in r.metadata["headline"] for r, distance in results)
    # Query for electric truck
    results = await db.search("truck", k=1)
    assert any("Tesla" in r.metadata["headline"] for r, distance in results)

@pytest.mark.asyncio
async def test_semantic_search_distance_filter(db: LangChainFAISSVectorDB):
    # Should only return results within threshold
    results = await db.search("grocery", k=5)
    assert any("Amazon" in r.metadata["headline"] and distance < 5 for r, distance in results)
    # Query for something not present
    results = await db.search("spaceX", k=5)
    assert not any(distance < 5 for r, distance in results)