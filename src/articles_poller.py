import asyncio
import time
import threading
import json
import os
from scraper import extract_article

# Monitor articles_urls.json for changes and fetch new articles
class ArticlesPoller:
    def __init__(self, poll_interval=2):
        self.poll_interval = poll_interval
        self.last_urls = set()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self.ready_event = threading.Event()

    async def start(self):
        self._thread.start()

    def _run(self):
        # Signal ready after first sync
        self.sync_new_articles()
        self.ready_event.set()
        while not self._stop_event.is_set():
            self.sync_new_articles()
            time.sleep(self.poll_interval)

    def sync_new_articles(self):
        new_urls = self.get_new_urls()
        for url in new_urls:
            try:
                article = asyncio.run(extract_article(url))
                self.add_article({
                    "url": article.url,
                    "headline": article.headline,
                    "text": article.text
                })
                print(f"Added raw article for {url}")
            except Exception as e:
                print(f"Failed to fetch article for {url}: {e}")

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


