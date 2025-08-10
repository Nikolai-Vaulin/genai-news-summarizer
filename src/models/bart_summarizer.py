from transformers import pipeline
from keybert import KeyBERT
import asyncio
from .summary_result import SummaryResult

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
kw_model = KeyBERT()

async def summarize_and_identify_topics(text):
    loop = asyncio.get_event_loop()
    def run():
        summary = summarizer(text, max_length=350, min_length=100, do_sample=False)[0]['summary_text']
        topics = [kw[0] for kw in kw_model.extract_keywords(summary, keyphrase_ngram_range=(1, 2), stop_words='english')]
        return SummaryResult(summary, topics)
    return await loop.run_in_executor(None, run)
