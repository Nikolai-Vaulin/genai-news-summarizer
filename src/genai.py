import json
import importlib
import asyncio

from src.models.bart_summarizer_class import BartSummarizer
from src.models.base import BaseSummarizer, BaseTopicsResolver
from src.models.keybert_topics_resolver import KeyBERTTopicsResolver
from src.models.openai_summarizer_class import OpenAISummarizer
from src.models.openai_topics_resolver import OpenAITopicsResolver
from src.models.t5_summarizer_class import T5Summarizer
from src.models.yake_topics_resolver import YakeTopicsResolver


def load_model_config():
    with open("model_config.json") as f:
        config = json.load(f)
    return config

config = load_model_config()

def get_summarizer() -> BaseSummarizer:
    model_name = config.get("summarizer_model", "openai")
    if model_name == "openai":
        return OpenAISummarizer()
    elif model_name == "bart":
        return BartSummarizer()
    elif model_name == "t5":
        return T5Summarizer()
    else:
        raise ValueError(f"Unknown model: {model_name}")

def get_topics_resolver() -> BaseTopicsResolver:
    model_name = config.get("topics_model", "keybert")
    if model_name == "keybert":
        return KeyBERTTopicsResolver()
    elif model_name == "openai":
        return OpenAITopicsResolver()
    elif model_name == "yake":
        return YakeTopicsResolver()
    else:
        raise ValueError(f"Unknown topics model: {model_name}")