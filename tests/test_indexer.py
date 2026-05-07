import pytest
from src.indexer import Indexer

# Test cases for the Indexer class using pytest
@pytest.fixture
# Sample indexer fixture to be used in multiple tests
def indexer():
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
    return idx
# Test tokenization of text into lowercase words without punctuation
def test_tokenization():
    idx = Indexer()
    text = "Hello, World! This is a test."
    tokens = idx.tokenize(text)
    assert tokens == ["hello", "world", "test"]
    assert idx.tokenize("Version 2 released") == ["version", "2", "releas"]  # Numbers should be included as tokens
    assert idx.tokenize("") == []  # Empty string should return an empty list of tokens
    assert idx.tokenize("   ") == []  # String with only whitespace should return an empty list of tokens#
    assert idx.tokenize("hello...world!!") == ["hello", "world"]  # Punctuation should be removed from tokens

# Test retrieval of postings
def test_case_insensitivity():

    idx = Indexer()

    content = [{
        "quote": "Hello World",
        "features": [
            {
                "text": "Hello World",
                "type": "text"
            }
        ]
    }]

    idx.add_document(
        "http://test.com",
        content
    )

    term = idx.tokenize("HELLO")[0]

    postings = idx.get_postings(term)

    assert len(postings) == 1

# Test term frequency by counting occurrences of a word in a document
def test_term_frequency():
    idx = Indexer()
    idx.add_document(1, [
        {
            "quote": "test test test",
            "features": [
                {
                    "text": "test test test",
                    "type": "text"
                }
            ]
        }
    ])
    postings = idx.get_postings("test")
    assert postings["0"]["score"] == 3  # The word "test" appears 3 times in the document
    assert postings["0"]["positions"] == [0, 1, 2]  # The positions of the word "test" in the document should be recorded correctly

# Test document frequency by counting the number of documents containing a word
def test_document_frequency(indexer):
    postings = indexer.get_postings("fox")
    assert len(postings) == 2

# Test missing words create empty postings lists without errors
def test_missing_word(indexer):
    postings = indexer.get_postings("nonexistent")
    assert postings == {}

# Test saving and loading the index to ensure data integrity across sessions
def test_save_load(tmp_path):
    idx = Indexer()
    idx.add_document(1, [
        {
            "quote": "Hello world",
            "features": [
                {
                    "text": "Hello world",
                    "type": "text"
                }
            ]
        }
    ])
    idx.add_document(2, [
        {
            "quote": "Another document",
            "features": [
                {
                    "text": "Another document",
                    "type": "text"
                }
            ]
        }
    ])
    
    file_path = tmp_path / "index.json"
    idx.save(file_path)
    
    new_idx = Indexer()
    new_idx.load(file_path)
    
    assert new_idx.index == idx.index
    assert new_idx.total_documents == idx.total_documents
    assert new_idx.get_postings("hello") == {
        "0": {
            "score": 1,
            "positions": [0]
        }
    }

# Test deduplication of quotes to ensure the same quote is not stored multiple times in the index
def test_deduplication():
    idx = Indexer()
    quote = {
        "quote": "Duplicate quote",
        "features": [
            {
                "text": "Duplicate quote",
                "type": "text"
            }
        ]
    }
    idx.add_document(1, [quote])
    idx.add_document(2, [quote])

    assert len(idx.quote_map) == 1  # Only one unique quote should be stored

    term = idx.tokenize("Duplicate quote")[0]
    postings = idx.get_postings(term)
    assert len(postings) == 2  # Both documents should reference the same quote

# Test the indexer handles similar words correctly by stemming them to their root form
def test_stemming():
    idx = Indexer()
    tokens = idx.tokenize("running runs runner")
    assert tokens == ["run", "run", "runner"]  # "running" and "runs" should be stemmed to "run"
    assert idx.tokenize("RUNNING") == ["run"]  # Stemming should be case-insensitive




