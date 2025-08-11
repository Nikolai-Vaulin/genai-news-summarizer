import asyncio
import time
import threading
import json
import os
import logging
from newspaper import Article
import asyncio
from src.models.article_result import ArticleResult


# Monitor articles_urls.json for changes and fetch new articles
class ArticlesPoller:
    def _thread_entry(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run())
        loop.close()

    logger = None

    def __init__(self, poll_interval=2):
        self._init_logger()
        self.poll_interval = poll_interval
        self.last_urls = set()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._thread_entry, daemon=True)
        self.ready_event = threading.Event()

    def _init_logger(self):
        if ArticlesPoller.logger is None:
            logger = logging.getLogger("ArticlesPoller")
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            if not logger.hasHandlers():
                logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            ArticlesPoller.logger = logger
        self.logger = ArticlesPoller.logger

    async def start(self):
        self._thread.start()

    def _run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run())
        loop.close()

    async def _run(self):
        # Signal ready after first sync
        await self.sync_new_articles()
        self.ready_event.set()
        while not self._stop_event.is_set():
            await asyncio.sleep(self.poll_interval)
            await self.sync_new_articles()

    async def sync_new_articles(self):
        new_urls = self.get_new_urls()
        for url in new_urls:
            try:
                article = await self._extract_article(url)
                self.add_article({
                    "url": article.url,
                    "headline": article.headline,
                    "text": article.text
                })
                self.logger.info(f"Added raw article for {url}")
            except Exception as e:
                self.logger.error(f"Failed to fetch article for {url}: {e}")

    async def _extract_article(self,url):
        article = Article(url)
        self.logger.info(f"Downloading article from {url}...")
        article.download()
        self.logger.info(f"Parsing article from {url}...")
        article.parse()
        return ArticleResult(url, article.title, article.text)

    @staticmethod
    def load_json(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_json(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_existing_urls(articles):
        return {a.get('url') for a in articles if 'url' in a}

    def get_new_urls(self):
        ARTICLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'articles')
        ARTICLES_JSON = os.path.join(ARTICLES_DIR, 'articles.json')
        URLS_JSON = os.path.join(ARTICLES_DIR, 'articles_urls.json')
        articles = self.load_json(ARTICLES_JSON)
        urls = self.load_json(URLS_JSON)
        existing_urls = self.get_existing_urls(articles)
        new_urls = [u for u in urls if u not in existing_urls]
        return new_urls

    def add_article(self, article):
        ARTICLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'articles')
        ARTICLES_JSON = os.path.join(ARTICLES_DIR, 'articles.json')
        articles = self.load_json(ARTICLES_JSON)
        articles.append(article)
        self.save_json(ARTICLES_JSON, articles)

    def stop(self):
        self._stop_event.set()
        self._thread.join()