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

    # Console input loop
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "Type command: ")
        cmd = user_input.strip().lower()
        if cmd.startswith("search"):
            query = user_input.strip()[6:].strip()
            if not query:
                print("Please provide search terms after 'search'.")
                continue
            print(f"Running semantic search for: {query}")
            from semantic_search import semantic_search
            results = await semantic_search(query, articles_processor.client)
            if not results:
                print("No results found.")
            else:
                for i, item in enumerate(results, 1):
                    print(f"Result {i}:")
                    print(f"  Headline: {item['headline']}")
                    print(f"  Summary: {item['summary']}")
                    print(f"  Topics: {item['topics']}")
                    print(f"  URL: {item['url']}")
        elif cmd in ("exit", "quit"):
            print("Exiting program...")
            articles_poller.stop()
            articles_processor.stop()
            break
        else:
            print("Unknown command. Type 'search <your query>' to search, or 'exit'/'quit' to close the app.")

if __name__ == "__main__":
    asyncio.run(main())
