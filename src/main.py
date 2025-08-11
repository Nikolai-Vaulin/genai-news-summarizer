import asyncio
from articles_poller import ArticlesPoller
from articles_processor import ArticlesProcessor
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from vector_dbs.FAISS_vector_db import LangChainFAISSVectorDB
from vector_dbs.base_vector_db import BaseVectorDB

async def main():
    # Start workers for articles and sync
    articles_poller = ArticlesPoller()
    await articles_poller.start()
    print("Waiting for articles poller to finish syncing articles...")
    articles_poller.ready_event.wait()
    print("Articles poller finished syncing. Waiting for articles processor...")
    vector_db_client = await create_vector_db_client()
    articles_processor = ArticlesProcessor(vector_db_client)
    await articles_processor.start()
    articles_processor.ready_event.wait()
    print("Articles processor finished syncing. You can now enter commands.")
    print("Workers started. Main app running...")

    await console_input_loop(articles_poller, articles_processor, vector_db_client)

async def console_input_loop(articles_poller, articles_processor, vector_db_client: BaseVectorDB):
    session = PromptSession("Type command: ")
    with patch_stdout():
        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, session.prompt)
            cmd = user_input.strip().lower()
            if cmd.startswith("search"):
                query = user_input.strip()[6:].strip()
                await search_query(query, vector_db_client)
            elif cmd in ("exit", "quit"):
                print("Exiting program...")
                articles_poller.stop()
                articles_processor.stop()
                break
            else:
                print("Unknown command. Type 'search <your query>' to search, or 'exit'/'quit' to close the app.")

async def search_query(query, vector_db_client: BaseVectorDB):
    if not query:
        print("Please provide search terms after 'search'.")
        return
    print(f"Running semantic search for: {query}")
    results = await semantic_search(query, vector_db_client)
    if not results:
        print("No results found.")
    else:
        for i, item in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Headline: {item['headline']}")
            print(f"  Summary: {item['summary']}")
            print(f"  Topics: {item['topics']}")
            print(f"  URL: {item['url']}")
            print(f"  Distance: {item['distance']}")

async def semantic_search(query, vector_db_client: BaseVectorDB):
    if not query:
        print("Please provide search terms after 'search'.")
        return
    print(f"Running semantic search for: {query}")
    results = await vector_db_client.search(query)
    items = [
                {
                    "summary": result.metadata.get("summary", ""),
                    "topics": result.metadata.get("topics", ""),
                    "headline": result.metadata.get("headline", ""),
                    "url": result.metadata.get("url", ""),
                    "distance": distance
                }
                for result, distance in results]

    if not items:
        print("No results found.")
    else:
        for i, item in enumerate(items, 1):
            print(f"Result {i}:")
            print(f"  Headline: {item['headline']}")
            print(f"  Summary: {item['summary']}")
            print(f"  Topics: {item['topics']}")
            print(f"  URL: {item['url']}")
            print(f"  Distance: {item['distance']}")

async def create_vector_db_client():
    return LangChainFAISSVectorDB()

if __name__ == "__main__":
    asyncio.run(main())
