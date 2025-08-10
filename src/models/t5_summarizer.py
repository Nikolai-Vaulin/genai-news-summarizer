from transformers import pipeline
import asyncio

summarizer = pipeline("summarization", model="t5-base")

async def get_summary(text):
    loop = asyncio.get_event_loop()
    def run():
        # Truncate input to 1024 tokens (T5's max input)
        input_max_length = 1024
        summary_max_length = 150  # Reasonable summary output length
        words = text.split()
        if len(words) > input_max_length:
            truncated_text = " ".join(words[:input_max_length])
        else:
            truncated_text = text
        summary_result = summarizer(
            truncated_text,
            max_length=summary_max_length,
            min_length=30,
            do_sample=False,
            truncation=True
        )
        if summary_result and 'summary_text' in summary_result[0]:
            summary_text = summary_result[0]['summary_text']
        else:
            summary_text = ""
        return summary_text
    return await loop.run_in_executor(None, run)
