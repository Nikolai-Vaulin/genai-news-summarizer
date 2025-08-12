import pytest
from src.models.t5_summarizer_class import T5Summarizer

def load_long_article():
    with open("tests/testData/long_article.txt", encoding="utf-8") as f:
        return f.read()

@pytest.mark.asyncio
async def test_t5_summarizer_various_lengths():
    text = load_long_article()
    summarizer = T5Summarizer()
    summary = await summarizer.summarize(text)
    assert isinstance(summary, str)
    assert len(summary) > 0
    if len(text) > 1024:
        assert len(summary) < len(text)
