import pytest
from src.indexer import Indexer
from src.search import Search

@pytest.fixture
# Fixture to create a Search instance with a pre-populated Indexer for testing
def search():
    idx = Indexer()
    idx.add_document(1, "The quick brown fox jumps over the lazy dog")
    idx.add_document(2, "The lazy dog is sleeping")
    idx.add_document(3, "The fox is quick and clever")
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
