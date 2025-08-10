import asyncio
import time
import threading
from articles_sync import load_json, ARTICLES_JSON
from genai import summarize_and_identify_topics
from vector_db import get_vector_db, add_article_to_db

class ArticlesProcessor:
    def __init__(self, poll_interval=2):
        self.poll_interval = poll_interval
        self.last_articles = None
        self.client = None
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        if self.client is None:
            raise RuntimeError("Call await init_client() before start()")
        self._thread.start()

    async def init_client(self):
        self.client = await get_vector_db()

    def _run(self):
        while not self._stop_event.is_set():
            self.sync_articles_db()
            time.sleep(self.poll_interval)

    def sync_articles_db(self):
        articles = load_json(ARTICLES_JSON)
        # Get existing article IDs from vector DB
        collection = self.client.get_or_create_collection("articles")
        try:
            existing_ids = set(collection.get(ids=None)["ids"])
        except Exception:
            existing_ids = set()
        for article in articles:
            article_id = article.get('url')
            if article_id in existing_ids:
                continue
            try:
                summary_with_topics = asyncio.run(summarize_and_identify_topics(article['text']))
                # Create a minimal ArticleResult for vector DB
                class ArticleResult:
                    def __init__(self, url, headline, text):
                        self.url = url
                        self.headline = headline
                        self.text = text
                article_obj = ArticleResult(article.get('url'), article.get('headline'), article.get('text'))
                asyncio.run(add_article_to_db(self.client, article_obj, summary_with_topics))
                print(f"Synced article {article.get('url')} with vector DB.")
            except Exception as e:
                print(f"Failed to sync article {article.get('url')}: {e}")

    def stop(self):
        self._stop_event.set()
        self._thread.join()
