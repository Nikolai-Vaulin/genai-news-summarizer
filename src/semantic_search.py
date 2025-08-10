import asyncio
from vector_db import get_articles_collection

async def semantic_search(query, client):
    """Perform semantic search using ChromaDB vector DB."""
    def sync_search():
        collection = get_articles_collection(client)
        results = collection.query(
            query_texts=[query],
            n_results=5,
            include=["documents", "metadatas"]
        )
        items = []
        for doc, meta in zip(results.get("documents", []), results.get("metadatas", [])):
            items.append({
                "summary": doc,
                "topics": meta.get("topics", ""),
                "headline": meta.get("headline", ""),
                "url": meta.get("url", "")
            })
        return items
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_search)
