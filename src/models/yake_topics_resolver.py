import yake
import asyncio
from .base import BaseTopicsResolver

class YakeTopicsResolver(BaseTopicsResolver):
    def __init__(self):
        self.kw_extractor = yake.KeywordExtractor()

    async def resolve_topics(self, text: str) -> list:
        loop = asyncio.get_event_loop()
        def run():
            keywords = self.kw_extractor.extract_keywords(text)
            return [kw for kw, score in keywords]
        return await loop.run_in_executor(None, run)