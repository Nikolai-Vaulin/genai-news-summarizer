import pytest
from src.vector_db import FaissVectorDB
from src.semantic_search import semantic_search
from src.FAISS_vector_db import LangChainFAISSVectorDB
import asyncio

@pytest.fixture
def db():
    # db = FaissVectorDB()
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
async def test_semantic_search_basic(db):
    # Query for a tech topic
    results = await semantic_search("iPhone", db)
    assert any("Apple" in r["headline"] for r in results)
    # Query for AI
    results = await semantic_search("AI", db)
    assert any("Microsoft" in r["headline"] for r in results)
    # Query for electric truck
    results = await semantic_search("truck", db)
    assert any("Tesla" in r["headline"] for r in results)

@pytest.mark.asyncio
async def test_semantic_search_distance_filter(db):
    # Should only return results within threshold
    results = await semantic_search("grocery", db, k=5, distance_threshold=3.0)
    assert any("Amazon" in r["headline"] for r in results)
    # Query for something not present
    results = await semantic_search("spaceX", db, k=5, distance_threshold=3.0)
    assert results == []

@pytest.mark.asyncio
async def test_semantic_search_keyword_fallback(db):
    # Query for exact word not semantically matched
    results = await semantic_search("Office", db, k=5, distance_threshold=3.0)
    # Should fallback to keyword match
    assert any("Microsoft" in r["headline"] for r in results)

@pytest.mark.asyncio
async def test_semantic_search_long_article(db):
    # Query for a long article
    results = await semantic_search("Putin Trump Summit", db, k=5, distance_threshold=3.0)
    # Should find the long article
    assert any("Putin" in r["headline"] for r in results)
