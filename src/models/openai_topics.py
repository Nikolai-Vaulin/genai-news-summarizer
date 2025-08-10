import openai
from config import OPENAI_API_KEY
import asyncio

client = openai.OpenAI(api_key=OPENAI_API_KEY)

async def extract_topics(text):
    loop = asyncio.get_event_loop()
    def run():
        prompt = f"List the main topics of the following article:\n\n{text}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        topics = response.choices[0].message.content.split('\n')
        return [t.strip() for t in topics if t.strip()]
    return await loop.run_in_executor(None, run)
