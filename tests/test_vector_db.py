from src.vector_db import get_vector_db

def test_get_vector_db():
    client = get_vector_db()
    assert client is not None
