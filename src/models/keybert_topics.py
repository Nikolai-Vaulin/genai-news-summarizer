from keybert import KeyBERT
import asyncio

kw_model = KeyBERT()

async def extract_topics(text):
    loop = asyncio.get_event_loop()
    def run():
        topics = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
        return [topic[0] for topic in topics]
    return await loop.run_in_executor(None, run)
