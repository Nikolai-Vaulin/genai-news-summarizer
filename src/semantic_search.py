import asyncio
from src.vector_db import BaseVectorDB

async def semantic_search(query, client: BaseVectorDB, k=3):
    """Perform semantic search using FAISS vector DB."""
    def sync_search():
        # Use FAISS IndexFlatIP and top-k search
        results = client.search(query, k=k)
        items = [
                    {
                        "summary": result.metadata.get("summary", ""),
                        "topics": result.metadata.get("topics", ""),
                        "headline": result.metadata.get("headline", ""),
                        "url": result.metadata.get("url", ""),
                        "distance": distance
                    }
                    for result, distance in results]
        # Keyword fallback if no semantic results
        # if not items:
        #     all_docs, all_metas = client.get_all()
        #     for doc, meta in zip(all_docs, all_metas):
        #         if query.lower() in doc.lower():
        #             items.append({
        #                 "summary": meta.get("summary", doc),
        #                 "topics": meta.get("topics", ""),
        #                 "headline": meta.get("headline", ""),
        #                 "url": meta.get("url", ""),
        #                 "distance": None
        #             })
        return items
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_search)
