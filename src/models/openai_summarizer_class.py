import openai
from config import OPENAI_API_KEY
import asyncio
from .base import BaseSummarizer

class OpenAISummarizer(BaseSummarizer):
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def summarize(self, text: str) -> str:
        loop = asyncio.get_event_loop()
        def run():
            prompt = f"Summarize the following article and list its main topics:\n\n{text}"
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message.content
            return summary
        return await loop.run_in_executor(None, run)
