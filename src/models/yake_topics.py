import yake
import asyncio

kw_extractor = yake.KeywordExtractor()

async def extract_topics(text):
    loop = asyncio.get_event_loop()
    def run():
        keywords = kw_extractor.extract_keywords(text)
        return [kw for kw, score in keywords]
    return await loop.run_in_executor(None, run)
