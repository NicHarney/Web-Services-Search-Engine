import pytest
from src.indexer import Indexer
from src.search import Search

@pytest.fixture
# Fixture to create a Search instance with a pre-populated Indexer for testing
def search():
    idx = Indexer()
    idx.add_document(1, [
        {
            "quote": "The quick brown fox jumps over the lazy dog",
            "features": [
                {
                    "text": "The quick brown fox jumps over the lazy dog",
                    "type": "text"
                }
            ]
        }
    ])
    idx.add_document(2, [
        {
            "quote": "The lazy dog is sleeping",
            "features": [
                {
                    "text": "The lazy dog is sleeping",
                    "type": "text"
                }
            ]
        }
    ])
    idx.add_document(3, [
        {
            "quote": "The fox is quick and clever",
            "features": [
                {
                    "text": "The fox is quick and clever",
                    "type": "text"
                }
            ]
        }
    ])
    return Search(idx)

# Testing single word search
def test_single_word(search):
    results = search.find("fox")
    assert set(results) == {"1", "3"}

# Testing multiple word search with AND strategy
def test_and_query(search):
    results = search.find("quick fox")
    assert set(results) == {"1", "3"}

def test_quoted_query_requires_adjacent_words(search):
    results = search.find('"quick fox"')
    assert results == []

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

# Testing ranking of search results
def test_ranking():
    idx = Indexer()
    idx.add_document(1, [
        {
            "quote": "life life life",
            "features": [
                {
                    "text": "life life life",
                    "type": "text"
                }
            ]
        }
    ])
    idx.add_document(2, [
        {
            "quote": "life",
            "features": [
                {
                    "text": "life",
                    "type": "text"
                }
            ]
        }
    ])

    search = Search(idx)
    results = search.find("life")

    assert set(results) == {"1", "2"}     

# Testing that the search returns all matching URLs for a given query term
def test_search_returns_all_urls():
    idx = Indexer()

    quote = {
        "quote": "Life is beautiful",
        "features": [
            {
                "text": "Life is beautiful",
                "type": "text"
            }
        ]
    }

    idx.add_document("url1", [quote])
    idx.add_document("url2", [quote])

    search = Search(idx)

    results = search.find("life")

    assert set(results) == {"url1", "url2"}

# Test weighting of terms based on HTML element type
def test_weighting():
    idx = Indexer()

    idx.add_document(1, [
        {
            "quote": "life",
            "features": [
                {
                    "text": "life",
                    "type": "text"
                }
            ]
        }
    ])

    idx.add_document(2, [
        {
            "quote": "life",
            "features": [
                {
                    "text": "life",
                    "type": "heading"
                }
            ]
        }
    ])

    idx.add_document(3, [
        {
            "quote": "life",
            "features": [
                {
                    "text": "life",
                    "type": "bold"
                }
            ]
        }
    ])

    search = Search(idx)

    results = search.find("life")

    assert set(results) == {"1", "2", "3"}

# Test phrase search
def test_phrase_search():
    idx = Indexer()

    idx.add_document(1, [
        {
            "quote": "life is beautiful",
            "features": [
                {
                    "text": "life is beautiful",
                    "type": "text"
                }
            ]
        }
    ])

    idx.add_document(2, [
        {
            "quote": "beautiful life is",
            "features": [
                {
                    "text": "beautiful life is",
                    "type": "text"
                }
            ]
        }
    ])

    search = Search(idx)

    results = search.find('"life is beautiful"')

    assert results == ["1"]

# Test phrase search with no match
def test_phrase_search_no_match():
    idx = Indexer()

    idx.add_document(1, [
        {
            "quote": "life is beautiful",
            "features": [
                {
                    "text": "life is beautiful",
                    "type": "text"
                }
            ]
        }
    ])

    search = Search(idx)

    results = search.find('"beautiful life"')

    assert results == []

# Test proximity boost ranking
def test_proximity_boost_ranking():
    idx = Indexer()
    idx.add_document(1, [
        {
            "quote": "good friends",
            "features": [
                {
                    "text": "good friends",
                    "type": "text"
                }
            ]
        }
    ])

    idx.add_document(2, [{
        "quote": "good and loyal friends",
        "features": [
            {
                "text": "good and loyal friends",
                "type": "text"
            }
        ]
    }])

    search = Search(idx)
    results = search.find("good friends")
    assert set(results) == {"1", "2"}

# Test stemming of search terms to match different forms of a word
def test_stemmed_search():
    idx = Indexer()

    idx.add_document(1, [
        {
            "quote": "I am running",
            "features": [
                {
                    "text": "I am running",
                    "type": "text"
                }
            ]
        }
    ])

    search = Search(idx)
    results = search.find("run")
    assert set(results) == {"1"}  # The search for "run" should match the document containing "running"