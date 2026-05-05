import json
import re

#  Inverted Indexer Implementation
class Indexer:

    # Initialize the indexer with an empty index and document count
    def __init__(self):
        self.index = {}
        self.total_documents = 0

        self.quote_map = {}
        self.quotes = {}
        self.next_id = 0

    def _get_or_create_quote_id(self, quote):
        if quote not in self.quote_map:
            quote_id = str(self.next_id)
            self.quote_map[quote] = quote_id
            self.quotes[quote_id] = {
                'quote': quote,
                'urls': set()
            }
            self.next_id += 1
        return self.quote_map[quote]
    
    # add a document to the indexer and update the index and document count
    def add_document(self, url, quotes):
        url = str(url)
        for quote in quotes:
            quote_id = self._get_or_create_quote_id(quote)
            self.quotes[quote_id]['urls'].add(url)

            words = self.tokenize(quote)

            for word in words:
                if word not in self.index:
                    self.index[word] = {}
                if quote_id not in self.index[word]:
                    self.index[word][quote_id] = 0
                self.index[word][quote_id] += 1
        self.total_documents = len(self.quotes)
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