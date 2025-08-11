import asyncio
from articles_poller import ArticlesPoller
from articles_processor import ArticlesProcessor
from semantic_search import semantic_search
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

async def main():
    # Start workers for articles and sync
    articles_poller = ArticlesPoller()
    articles_processor = ArticlesProcessor()
    await articles_poller.start()
    await articles_processor.start()
    print("Waiting for articles poller to finish syncing articles...")
    articles_poller.ready_event.wait()
    print("Articles poller finished syncing. Waiting for articles processor...")
    articles_processor.ready_event.wait()
    print("Articles processor finished syncing. You can now enter commands.")
    print("Workers started. Main app running...")

    await console_input_loop(articles_poller, articles_processor)

async def console_input_loop(articles_poller, articles_processor):
    session = PromptSession("Type command: ")
    with patch_stdout():
        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, session.prompt)
            cmd = user_input.strip().lower()
            if cmd.startswith("search"):
                query = user_input.strip()[6:].strip()
                if not query:
                    print("Please provide search terms after 'search'.")
                    continue
                print(f"Running semantic search for: {query}")
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
