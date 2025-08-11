import faiss
from abc import ABC, abstractmethod
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

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
    def search(self, query, k=5):
        pass

    def get_all(self):
        return self.docs, self.metas
