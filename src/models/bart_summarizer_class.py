from transformers import pipeline
from .base import BaseSummarizer
import asyncio

class BartSummarizer(BaseSummarizer):
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    async def summarize(self, text: str) -> str:
        loop = asyncio.get_event_loop()
        def run():
            input_max_length = 512
            words = text.split()
            if len(words) > input_max_length:
                truncated_text = " ".join(words[:input_max_length])
            else:
                truncated_text = text
            summary_max_length = min(200, len(truncated_text.split()))
            summary_result = self.summarizer(
                truncated_text,
                max_length=summary_max_length,
                min_length=30,
                do_sample=False
            )
            if summary_result and 'summary_text' in summary_result[0]:
                summary_text = summary_result[0]['summary_text']
            else:
                summary_text = ""
            return summary_text
        return await loop.run_in_executor(None, run)
