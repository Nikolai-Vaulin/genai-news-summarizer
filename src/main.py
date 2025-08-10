import asyncio
from scraper import extract_article
from genai import summarize_and_identify_topics
from vector_db import get_vector_db, add_article_to_db
from semantic_search import semantic_search

async def main():
    urls = [
        # Add your news URLs here
        "https://www.nytimes.com/2025/08/08/us/trump-military-drug-cartels.html"
    ]
    client = await get_vector_db()
    for url in urls:
        article = await extract_article(url)
        summary_with_topics = await summarize_and_identify_topics(article.text)
        await add_article_to_db(client, article, summary_with_topics)
    # Example search
    results = await semantic_search("military", client)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
