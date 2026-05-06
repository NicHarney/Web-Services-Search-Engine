import pytest
from src.indexer import Indexer
from src.search import Search

@pytest.fixture
# Fixture to create a Search instance with a pre-populated Indexer for testing
def search():
    idx = Indexer()
    idx.add_document(1, [{"text": "The quick brown fox jumps over the lazy dog", "type": "text"}])
    idx.add_document(2, [{"text": "The lazy dog is sleeping", "type": "text"}])
    idx.add_document(3, [{"text": "The fox is quick and clever", "type": "text"}])
    return Search(idx)

# Testing single word search
def test_single_word(search):
    results = search.find("fox")
    assert set(results) == {"1", "3"}

# Testing multiple word search with AND strategy
def test_and_query(search):
    results = search.find("quick fox")
    assert set(results) == {"1", "3"}

# Testing case insensitivity of search queries
def test_case_insensitivity(search):
    results = search.find("QUICK")
    assert set(results) == {"1", "3"}

# Testing search with a word that does not exist in any document
def test_no_match(search):
    results = search.find("cat")
    assert results == []

# Testing search with an empty query should return an empty result
def test_empty_query(search):
    results = search.find("")
    assert results == []

def test_ranking():
    idx = Indexer()
    idx.add_document(1, [{"text": "life life life", "type": "text"}])
    idx.add_document(2, [{"text": "life", "type": "text"}])

    search = Search(idx)
    results = search.find("life")

    assert set(results) == {"1", "2"}     

def test_search_returns_all_urls():
    idx = Indexer()

    quote = {"text": "Life is beautiful", "type": "text"}

    idx.add_document("url1", [quote])
    idx.add_document("url2", [quote])

    search = Search(idx)

    results = search.find("life")

    assert set(results) == {"url1", "url2"}

def test_weighting():
    idx = Indexer()

    idx.add_document(1, [{"text": "life", "type": "text"}])

    idx.add_document(2,[{"text": "life", "type": "heading"}])

    idx.add_document(3, [{"text": "life", "type": "bold"}])

    search = Search(idx)

    results = search.find("life")

    assert results[0][0] == "2"  # Heading should have the highest weight
    assert results[1][0] == "3"  # Bold should have the second highest weight
    assert results[2][0] == "1"  # Text should have the lowest weight