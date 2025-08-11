import asyncio
import time
import threading
import logging
from articles_sync import load_json, ARTICLES_JSON
from genai import summarize_and_identify_topics
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.vector_dbs.base_vector_db import BaseVectorDB
from src.vector_dbs.article_result import ArticleResult

class ArticlesProcessor:
    logger = None
    def __init__(self, client: BaseVectorDB, poll_interval=2):
        self._init_logger()
        self.client = client
        self.poll_interval = poll_interval
        self.last_articles = None
        self._stop_event = threading.Event()
        self.ready_event = threading.Event()
        self._thread = threading.Thread(target=self._thread_entry, daemon=True)
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            chunk_overlap=50,
            length_function=len
        )

    def _init_logger(self):
        if ArticlesProcessor.logger is None:
            logger = logging.getLogger("ArticlesProcessor")
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            if not logger.hasHandlers():
                logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            ArticlesProcessor.logger = logger
        self.logger = ArticlesProcessor.logger

    async def start(self):
        self._thread.start()

    def _thread_entry(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run())
        loop.close()

    async def _run(self):
        await self.sync_articles_db()
        self.ready_event.set()
        while not self._stop_event.is_set():
            await self.sync_articles_db()
            await asyncio.sleep(self.poll_interval)

    async def sync_articles_db(self):
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
                await self._process_article(article)
            except Exception as e:
                self.logger.error(f"Failed to sync article {article.get('url')}: {e}")
        self.logger.info("Finished syncing articles with vector DB.")

    async def _process_article(self, article):
        self.logger.info(f"Processing article {article.get('url')}...")
        chunks = self._text_splitter.split_text(article['text'])
        self.logger.info(f"Split into {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
            self.logger.info(f"Processing chunk {i + 1}/{len(chunks)}...")
            summary_with_topics = await summarize_and_identify_topics(chunk)
            self.logger.info(f"Summary: {summary_with_topics.summary[:50]}... Topics: {summary_with_topics.topics}")
            article_obj = ArticleResult(article.get('url'), article.get('headline'), chunk)
            self.logger.info(f"Adding article {article.get('url')} to vector DB...")
            await self.client.add_article_to_db(article_obj, summary_with_topics)
        self.logger.info(f"Synced article {article.get('url')} with vector DB.")
    
    def stop(self):
        self._stop_event.set()
        self._thread.join()
