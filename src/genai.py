import json
import importlib
import asyncio

from src.models.summary_result import SummaryResult

def load_model_config():
    with open("model_config.json") as f:
        config = json.load(f)
    return config

def get_summary_func(model_name):
    if model_name == "openai":
        module = importlib.import_module("src.models.openai_summarizer")
        return module.get_summary
    elif model_name == "bart":
        module = importlib.import_module("src.models.bart_summarizer")
        return module.get_summary
    elif model_name == "t5":
        module = importlib.import_module("src.models.t5_summarizer")
        return module.get_summary
    else:
        raise ValueError(f"Unknown model: {model_name}")

def get_topics_model_func(model_name):
    if model_name == "keybert":
        module = importlib.import_module("src.models.keybert_topics")
        return module.extract_topics
    elif model_name == "openai":
        module = importlib.import_module("src.models.openai_topics")
        return module.extract_topics
    elif model_name == "yake":
        module = importlib.import_module("src.models.yake_topics")
        return module.extract_topics
    else:
        raise ValueError(f"Unknown topics model: {model_name}")

async def summarize_and_identify_topics(text):
    config = load_model_config()
    model_func = get_summary_func(config.get("summarizer_model", "openai"))
    topics_func = get_topics_model_func(config.get("topics_model", "keybert"))
    # Get summary
    if asyncio.iscoroutinefunction(model_func):
        summary_result = await model_func(text)
    else:
        loop = asyncio.get_event_loop()
        summary_result = await loop.run_in_executor(None, model_func, text)
    # Get topics
    if asyncio.iscoroutinefunction(topics_func):
        topics = await topics_func(text)
    else:
        loop = asyncio.get_event_loop()
        topics = await loop.run_in_executor(None, topics_func, text)
    # Attach topics to summary_result if possible
    return SummaryResult(summary_result, topics)
