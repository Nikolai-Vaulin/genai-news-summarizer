import pytest
import asyncio
from src.genai import summarize_and_identify_topics

@pytest.mark.asyncio
async def test_summarize_and_identify_topics():
    text = "This is a test article about AI and technology."
    result = await summarize_and_identify_topics(text)
    # Check for custom result type and topics
    assert hasattr(result, 'summary') or hasattr(result, 'text')
    assert hasattr(result, 'topics')
    assert isinstance(result.topics, list)
