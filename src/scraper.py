from newspaper import Article
import asyncio
from src.models.article_result import ArticleResult

async def extract_article(url):
    """Extract headline and full text from a news article URL asynchronously using newspaper3k."""
    def get_article():
        article = Article(url)
        article.download()
        article.parse()
        return ArticleResult(url, article.title, article.text)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_article)
