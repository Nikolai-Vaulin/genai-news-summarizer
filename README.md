# GenAI News Summarizer

A GenAI-powered news summarizer with async workers, modular vector DB, configurable summarizers and topic resolvers, and an interactive console.

## Features

- Async/threaded worker startup
- Modular vector DB (FAISS)
- Structured logging
- Interactive console (prompt_toolkit)
- Summarization and topic extraction
- Configurable summarizers and topics resolvers

## Usage

1. Configure articles by adding URLs to `articles_urls.json` (the poller will fetch and update data automatically), or manually add articles to `articles.json`.
2. Run `main.py` to start the app.
3. Use the interactive console to search, view summaries, or interact with the summarizer.

## Environment Configuration

If you want to use OpenAI-based summarizers ortopics resolvers, you must set the `OPENAI_API_KEY` parameter in your `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Requirements

- Python 3.13+
- FAISS
- transformers
- prompt_toolkit
- langchain
- newspaper3k

## Project Structure

```
config.py
README.md
requirements.txt
data/
   articles.json
src/
   genai.py
   main.py
   scraper.py
   semantic_search.py
   articles_processor.py
   articles_poller.py
   vector_dbs/
      base_vector_db.py
      vector_db.py
      FAISS_vector_db.py
      article_result.py
   models/
      bart_summarizer_class.py
      t5_summarizer_class.py
      openai_summarizer_class.py
      keybert_topics_resolver.py
      openai_topics_resolver.py
      yake_topics_resolver.py
      base.py
tests/
   test_genai.py
   test_scraper.py
   test_semantic_search.py
   test_vector_db.py
```

## Customization

You can configure which summarizer and topics resolver to use by editing the `model_config.json` file. This file allows you to specify which summarizer and topics resolver should be used by the application at runtime, making it easy to switch between supported models without changing code.

See `base.py` for abstract base classes and available implementations. Supported summarizers include BART, T5, and OpenAI; supported topic resolvers include KeyBERT, YAKE, and OpenAI.

## Vector DB

This project uses FAISS as the vector database for semantic search and storage of article embeddings.

## Chunking

Articles are automatically split into manageable text chunks before summarization and vectorization. This improves processing and search accuracy.

## Adding Articles

- To add new article URLs, manually edit `articles_urls.json`. The articles poller will automatically fetch and update data.
- You can also add articles directly by editing `articles.json`.

## Console

After startup, use the interactive console to search articles, view summaries, or interact with the system.

## Available Console Commands

After starting the application, you can use the following commands in the interactive console:

- `search <query>`: Perform a semantic search for articles matching the query.
   - For each search request, three results are displayed, ordered by distance. In the context of a vector database, "distance" refers to how similar the article's embedding is to your query: a smaller distance means higher similarity.
   - The threshold for matching depends on the Tokenizer and AutoModel used. Currently, the project uses `sentence-transformers/distiluse-base-multilingual-cased-v2`.
   - Future plans include making the model and threshold configurable.
- `exit` or `quit`: Exit the application.
Planned: In future versions, console commands will be added to allow users to add article URLs and articles directly from the interactive console.

## Future Plans / TODO

- Add more tests to cover additional cases and improve reliability.
- Investigate and experiment with different embedding methods to decrease the distance in semantic search results. Currently, search results often start with a higher distance than expected.

## License

MIT
