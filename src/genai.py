import json
import importlib
import asyncio

def load_model_config():
    with open("model_config.json") as f:
        config = json.load(f)
    return config.get("summarizer_model", "openai")

def get_model_func(model_name):
    if model_name == "openai":
        module = importlib.import_module("src.models.openai_summarizer")
    elif model_name == "bart":
        module = importlib.import_module("src.models.bart_summarizer")
    elif model_name == "t5":
        module = importlib.import_module("src.models.t5_summarizer")
    elif model_name == "keybert":
        module = importlib.import_module("src.models.keybert_topics")
    else:
        raise ValueError(f"Unknown model: {model_name}")
    return module.summarize_and_identify_topics

async def summarize_and_identify_topics(text):
    model_name = load_model_config()
    model_func = get_model_func(model_name)
    # If the model is async, await it; else, run in executor
    if asyncio.iscoroutinefunction(model_func):
        return await model_func(text)
    else:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, model_func, text)
