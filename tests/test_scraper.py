from src.scraper import extract_article

def test_extract_article():
    url = "https://example.com/news"
    result = extract_article(url)
    assert "headline" in result and "text" in result
