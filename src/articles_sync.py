import json
import os

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'articles')
ARTICLES_JSON = os.path.join(ARTICLES_DIR, 'articles.json')
URLS_JSON = os.path.join(ARTICLES_DIR, 'articles_urls.json')

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_existing_urls(articles):
    return {a.get('url') for a in articles if 'url' in a}

def get_new_urls():
    articles = load_json(ARTICLES_JSON)
    urls = load_json(URLS_JSON)
    existing_urls = get_existing_urls(articles)
    new_urls = [u for u in urls if u not in existing_urls]
    return new_urls

def add_article(article):
    articles = load_json(ARTICLES_JSON)
    articles.append(article)
    save_json(ARTICLES_JSON, articles)