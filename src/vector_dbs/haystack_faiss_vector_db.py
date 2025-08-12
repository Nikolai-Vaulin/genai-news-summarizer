from haystack.document_stores.in_memory import InMemoryDocumentStore
from src.vector_dbs.base_vector_db import BaseVectorDB
from haystack import Document
from haystack.nodes import EmbeddingRetriever

class HaystackFAISSVectorDB(BaseVectorDB):
    def __init__(self, dim=768):
        super().__init__(dim)
        self.faiss_db = InMemoryDocumentStore(bm25_algorithm="BM25Plus")
        self.retriever = EmbeddingRetriever(document_store=self.faiss_db, embedding_model="sentence-transformers/all-MiniLM-L6-v2")

    def add(self, doc, meta, id):
        self.docs.append(doc)
        self.metas.append(meta)
        self.ids.append(id)
        document = Document(
            content=doc,
            meta=meta
        )
        self.faiss_db.write_documents([document])
        self.faiss_db.update_embeddings(self.retriever)

    async def search(self, query, k=5):
        results = await self.retriever.retrieve(query, top_k=k)
        return results