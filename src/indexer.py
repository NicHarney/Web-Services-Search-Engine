import json
import re

#  Inverted Indexer Implementation
class Indexer:

    # Initialize the indexer with an empty index and document count
    def __init__(self):
        self.index = {}
        self.total_documents = 0
    
    # add a document to the indexer and update the index and document count
    def add_document(self, document_id, text):
        # Convert document_id to string for consistent indexing
        document_id = str(document_id)
        words = self.tokenize(text)
        self.total_documents += 1

        # Update the index with the term frequencies for each word in the document
        for word in words:
            if word not in self.index:
                self.index[word] = {}
            if document_id not in self.index[word]:
                self.index[word][document_id] = 0
            self.index[word][document_id] += 1
    
    # tokenize text to lowercase words and remove punctuation
    def tokenize(self, text):
        text = text.lower()
        return re.findall(r'\b\w+\b', text)    
    
    # Retrieve the postings list for a given term, returning an empty dictionary if the term is not found
    def get_postings(self, term):
        word = term.lower()
        return self.index.get(word, {})
    
    # Save the index and document count to a JSON file
    def save(self, filepath):
        with open(filepath, 'w') as f:
            json.dump({
                'index': self.index,
                'total_documents': self.total_documents
            }, f)
    # Load the index and document count from a JSON file
    def load(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.index = data['index']
            self.total_documents = data['total_documents']

DOCS = {
    1: "The quick brown fox jumps over the lazy dog",
    2: "The lazy dog is sleeping",
    3: "The fox is quick and clever"
}