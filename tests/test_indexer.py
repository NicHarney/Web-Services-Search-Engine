import pytest
from src.indexer import Indexer

# Test cases for the Indexer class using pytest
@pytest.fixture
# Sample indexer fixture to be used in multiple tests
def indexer():
    idx = Indexer()
    idx.add_document(1, "The quick brown fox jumps over the lazy dog")
    idx.add_document(2, "The lazy dog is sleeping")
    idx.add_document(3, "The fox is quick and clever")
    return idx
# Test tokenization of text into lowercase words without punctuation
def test_tokenization():
    idx = Indexer()
    text = "Hello, World! This is a test."
    tokens = idx.tokenize(text)
    assert tokens == ['hello', 'world', 'this', 'is', 'a', 'test']

# Test retrieval of postings
def test_case_insensitivity(indexer):
    postings = indexer.get_postings("the")
    assert "1" in postings
    assert "2" in postings
    assert "3" in postings

# Test term frequency by counting occurrences of a word in a document
def test_term_frequency():
    idx = Indexer()
    idx.add_document(1, "test test test")
    postings = idx.get_postings("test")
    assert postings["1"] == 3

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
    idx.add_document(1, "Hello world")
    idx.add_document(2, "Another document")
    
    file_path = tmp_path / "index.json"
    idx.save(file_path)
    
    new_idx = Indexer()
    new_idx.load(file_path)
    
    assert new_idx.index == idx.index
    assert new_idx.total_documents == idx.total_documents
    assert new_idx.get_postings("hello") == {"1": 1}

