import asyncio
import faiss
from abc import ABC, abstractmethod
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from src.models.article_result import ArticleResult
from src.models.summary_result import SummaryResult

class BaseVectorDB(ABC):
    def __init__(self, dim=384, model_name="sentence-transformers/distiluse-base-multilingual-cased-v2"):
        self.dim = dim
        self.embeddings = []
        self.docs = []
        self.metas = []
        self.ids = []
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.index = faiss.IndexFlatL2(dim)

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            model_output = self.model(**inputs)
        embeddings = model_output.last_hidden_state.mean(dim=1).cpu().numpy()
        emb = embeddings[0]
        # No normalization for L2
        return emb

    @abstractmethod
    def add(self, doc, meta, id):
        pass

    @abstractmethod
    async def search(self, query, k=5):
        pass

    def get_all(self):
        return self.docs, self.metas

    @staticmethod
    def build_metadata(article: ArticleResult, summary: SummaryResult):
        return {
            "url": article.url,
            "headline": article.headline,
            "topics": summary.topics,
            "summary": summary.summary
        }

    async def add_article_to_db(self, article: ArticleResult, summary_with_topics: SummaryResult):
        meta = self.build_metadata(article, summary_with_topics)
        self.add(article.text, meta, article.url)