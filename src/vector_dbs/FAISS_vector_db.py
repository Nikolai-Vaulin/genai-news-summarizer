from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
import faiss

from src.vector_dbs.base_vector_db import BaseVectorDB

class LangChainFAISSVectorDB(BaseVectorDB):
    def __init__(self):
        super().__init__()
        docstore = InMemoryDocstore({})
        index_to_docstore_id = {}
        self.faiss_db = FAISS(embedding_function=self.embed, index=self.index, docstore=docstore, index_to_docstore_id=index_to_docstore_id)

    def add(self, doc, meta, id):
        self.docs.append(doc)
        self.metas.append(meta)
        self.ids.append(id)
        self.faiss_db.add_texts([doc], metadatas=[meta])

    async def search(self, query, k=5):
        results = self.faiss_db.similarity_search_with_score(query, k=k)
        return results
