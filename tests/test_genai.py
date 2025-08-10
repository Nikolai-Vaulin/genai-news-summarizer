from src.genai import summarize_and_identify_topics

def test_summarize_and_identify_topics():
    text = "This is a test article about AI and technology."
    summary = summarize_and_identify_topics(text)
    assert isinstance(summary, str)
