import asyncio
from vector_db import get_articles_collection

async def semantic_search(query, client):
    """Perform semantic search using ChromaDB vector DB."""
    def sync_search():
        collection = get_articles_collection(client)
        results = collection.query(
            query_texts=[query],
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )
        items = []
        docs_list = results.get("documents", [[]])
        metas_list = results.get("metadatas", [[]])
        distances_list = results.get("distances", [[]])
        threshold = 0.7
        for docs, metas, dists in zip(docs_list, metas_list, distances_list):
            for doc, meta, dist in zip(docs, metas, dists):
                if dist <= threshold:
                    items.append({
                        "summary": doc,
                        "topics": meta.get("topics", ""),
                        "headline": meta.get("headline", ""),
                        "url": meta.get("url", ""),
                        "distance": dist
                    })
        # Keyword fallback if no semantic results
        if not items:
            # Get all articles from the collection
            all_results = collection.get(
                include=["documents", "metadatas"]
            )
            all_docs = all_results.get("documents", [])
            all_metas = all_results.get("metadatas", [])
            for doc, meta in zip(all_docs, all_metas):
                if query.lower() in doc.lower():
                    items.append({
                        "summary": doc,
                        "topics": meta.get("topics", ""),
                        "headline": meta.get("headline", ""),
                        "url": meta.get("url", ""),
                        "distance": None  # No distance for keyword match
                    })
        return items
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_search)
