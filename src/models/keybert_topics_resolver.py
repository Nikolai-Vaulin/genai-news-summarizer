from keybert import KeyBERT
from .base import BaseTopicsResolver
import asyncio

class KeyBERTTopicsResolver(BaseTopicsResolver):
    def __init__(self):
        self.kw_model = KeyBERT()

    async def resolve_topics(self, text: str) -> list:
        loop = asyncio.get_event_loop()
        def run():
            topics = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
            return [topic[0] for topic in topics]
        return await loop.run_in_executor(None, run)
