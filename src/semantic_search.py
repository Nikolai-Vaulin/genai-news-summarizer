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
        # ChromaDB returns lists of lists for documents and metadatas
        docs_list = results.get("documents", [[]])
        metas_list = results.get("metadatas", [[]])
        # For each query (usually one), iterate over results
        for docs, metas in zip(docs_list, metas_list):
            for doc, meta in zip(docs, metas):
                items.append({
                    "summary": doc,
                    "topics": meta.get("topics", ""),
                    "headline": meta.get("headline", ""),
                    "url": meta.get("url", "")
                })
        return items
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_search)
