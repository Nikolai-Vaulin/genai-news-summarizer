import asyncio
from articles_poller import ArticlesPoller
from articles_processor import ArticlesProcessor

async def main():
    # Start workers for articles and sync
    articles_poller = ArticlesPoller()
    articles_processor = ArticlesProcessor()
    await articles_processor.init_client()
    articles_poller.start()
    articles_processor.start()
    print("Workers started. Main app running...")
    # Main app logic can go here
    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
