from transformers import pipeline
import asyncio
from .summary_result import SummaryResult

summarizer = pipeline("summarization", model="t5-small")

async def summarize_and_identify_topics(text):
    loop = asyncio.get_event_loop()
    def run():
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        topics = [s.strip() for s in summary.split('.') if s.strip()]
        return SummaryResult(summary, topics)
    return await loop.run_in_executor(None, run)
