import openai
from config import OPENAI_API_KEY
import asyncio
from .base import BaseTopicsResolver

class OpenAITopicsResolver(BaseTopicsResolver):
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def resolve_topics(self, text: str) -> list:
        loop = asyncio.get_event_loop()
        def run():
            prompt = f"List the main topics of the following article:\n\n{text}"
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            topics = response.choices[0].message.content.split('\n')
            return [t.strip() for t in topics if t.strip()]
        return await loop.run_in_executor(None, run)
