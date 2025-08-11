import pytest
from src.models.bart_summarizer import get_summary


def load_long_article():
    with open("tests/testData/long_article.txt", encoding="utf-8") as f:
        return f.read()

def load_short_article():
    return "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate"

@pytest.mark.asyncio
async def test_bart_summarizer_long_article_length():
    text = load_long_article()
    summary = await get_summary(text)
    assert isinstance(summary, str)
    assert len(summary) > 0

@pytest.mark.asyncio
async def test_bart_summarizer_short_article_length():
    text = load_short_article()
    summary = await get_summary(text)
    assert isinstance(summary, str)
    assert len(summary) > 0