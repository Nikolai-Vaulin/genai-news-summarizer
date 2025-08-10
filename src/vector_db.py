import chromadb
from chromadb.config import Settings
from config import VECTOR_DB_PATH
import os
import asyncio
from src.models.article_result import ArticleResult
from src.models.summary_result import SummaryResult

ARTICLES_COLLECTION_NAME = "articles"

def get_articles_collection(client):
    """Get or create the 'articles' collection from the vector DB client."""
    return client.get_or_create_collection(ARTICLES_COLLECTION_NAME)

def build_metadata(article: ArticleResult, summary: SummaryResult):
    return {
        "url": article.url,
        "headline": article.headline,
        "topics": summary.get_topics_str()
    }

async def get_vector_db():
    """Initialize and return a Chroma vector database client asynchronously, using VECTOR_DB_PATH for persistent storage."""
    # Ensure the data directory exists
    if not os.path.exists(VECTOR_DB_PATH):
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    loop = asyncio.get_event_loop()
    client = await loop.run_in_executor(None, lambda: chromadb.PersistentClient(path=VECTOR_DB_PATH))
    return client

async def add_article_to_db(client, article: ArticleResult, summary_with_topics: SummaryResult): 
    """Add article and summary to vector DB asynchronously."""
    # Example: add to a collection (replace with your actual logic)
    def sync_add():
        collection = get_articles_collection(client)
        meta = build_metadata(article, summary_with_topics)
        doc = summary_with_topics.summary
        collection.add(
            documents=[doc],
            metadatas=[meta],
            ids=[article.url]
        )
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sync_add)

