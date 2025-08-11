import asyncio
import time
import threading
from articles_sync import load_json, ARTICLES_JSON
from genai import summarize_and_identify_topics
from vector_db import get_vector_db, add_article_to_db
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ArticlesProcessor:
    def __init__(self, poll_interval=2):
        self.poll_interval = poll_interval
        self.last_articles = None
        self.client = None
        self._stop_event = threading.Event()
        self.ready_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            chunk_overlap=50,
            length_function=len
        )


    async def start(self):
        if self.client is None:
            self.client = await get_vector_db()
        self._thread.start()

    def _run(self):
        while not self._stop_event.is_set():
            self.sync_articles_db()
            time.sleep(self.poll_interval)

    def sync_articles_db(self):
        articles = load_json(ARTICLES_JSON)
        # Get existing article IDs from FAISS DB
        try:
            existing_ids = set(self.client.ids)
        except Exception:
            existing_ids = set()
        for article in articles:
            article_id = article.get('url')
            if article_id in existing_ids:
                continue
            try:
                print(f"Processing article {article.get('url')}...")
                chunks = self._text_splitter.split_text(article['text'])
                print(f"Split into {len(chunks)} chunks.    ")
                for i, chunk in enumerate(chunks):
                    print(f"Processing chunk {i + 1}/{len(chunks)}...")
                    summary_with_topics = asyncio.run(summarize_and_identify_topics(chunk))
                    print(f"Summary: {summary_with_topics.summary[:50]}... Topics: {summary_with_topics.topics}")
                    # Create a minimal ArticleResult for vector DB
                    class ArticleResult:
                        def __init__(self, url, headline, text):
                            self.url = url
                            self.headline = headline
                            self.text = text
                    article_obj = ArticleResult(article.get('url'), article.get('headline'), chunk)
                    print(f"Adding article {article.get('url')} to vector DB...")
                    asyncio.run(add_article_to_db(self.client, article_obj, summary_with_topics))
                print(f"Synced article {article.get('url')} with vector DB.")
            except Exception as e:
                print(f"Failed to sync article {article.get('url')}: {e}")
        self.ready_event.set()
    
    def stop(self):
        self._stop_event.set()
        self._thread.join()
