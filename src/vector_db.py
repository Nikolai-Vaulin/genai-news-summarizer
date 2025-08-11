# FAISS-based vector DB implementation
import faiss
import numpy as np
import torch
import asyncio
from src.models.article_result import ArticleResult
from src.models.summary_result import SummaryResult
from src.FAISS_vector_db import LangChainFAISSVectorDB
from src.base_vector_db import BaseVectorDB

class FaissVectorDB(BaseVectorDB):
    def __init__(self, dim=384):
        super().__init__(dim)
        # Use L2 distance

    def add(self, doc, meta, id):
        emb = self.embed(doc)
        self.index.add(np.array([emb]).astype(np.float32))
        self.embeddings.append(emb)
        self.docs.append(doc)
        self.metas.append(meta)
        self.ids.append(id)

    def search(self, query, k=5):
        emb = self.embed(query)
        D, I = self.index.search(np.array([emb]).astype(np.float32), k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < len(self.docs):
                results.append({
                    "summary": self.docs[idx],
                    "topics": self.metas[idx].get("topics", ""),
                    "headline": self.metas[idx].get("headline", ""),
                    "url": self.metas[idx].get("url", ""),
                    "distance": dist
                })
        return results

def build_metadata(article: ArticleResult, summary: SummaryResult):
    return {
        "url": article.url,
        "headline": article.headline,
        "topics": summary.topics,
        "summary": summary.summary
    }

async def get_vector_db():
    # Return a singleton FAISS DB instance
    if not hasattr(get_vector_db, "db"):
        get_vector_db.db = LangChainFAISSVectorDB()
    return get_vector_db.db

async def add_article_to_db(client: BaseVectorDB, article: ArticleResult, summary_with_topics: SummaryResult):
    def sync_add():
        meta = build_metadata(article, summary_with_topics)
        client.add(article.text, meta, article.url)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sync_add)

