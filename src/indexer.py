import json
import re
import os

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
            return quote_id, True
        return self.quote_map[quote], False
    
    # add a document to the indexer and update the index and document count
    def add_document(self, url, content):
        url = str(url)
        for item in content:
           quote_text = item['quote']
           quote_id, is_new = self._get_or_create_quote_id(quote_text)

           self.quotes[quote_id]['urls'].add(url)

           if not is_new:
               continue  # Skip re-indexing if the quote already exists
           current_position = 0
           for feature in item['features']:
                text = feature['text']
                feature_type = feature['type']
                weight = HTML_WEIGHTS.get(feature_type, 1)
                words = self.tokenize(text)
                for word in words:
                    if word not in self.index:
                        self.index[word] = {}
                    if quote_id not in self.index[word]:
                        self.index[word][quote_id] = {
                            "score": 0,
                            "positions": []
                        }
                    self.index[word][quote_id]['score'] += weight
                    self.index[word][quote_id]['positions'].append(current_position)
                    current_position += 1
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
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        serialized_quotes = {}
        for quote_id, quote_data in self.quotes.items():
            serialized_quotes[quote_id] = {
                'quote': quote_data['quote'],
                'urls': list(quote_data['urls'])
            }
        with open(filepath, 'w') as f:

            json.dump({
                'index': self.index,
                'quotes': serialized_quotes,
                'quote_map': self.quote_map,
                'total_documents': self.total_documents,
                'next_id': self.next_id
                
            }, f)
    # Load the index and document count from a JSON file
    def load(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.index = data['index']
        self.quote_map = data['quote_map']
        self.total_documents = data['total_documents']
        self.next_id = data['next_id']

        self.quotes = {}
        for quote_id, quote_data in data['quotes'].items():
            self.quotes[quote_id] = {
                'quote': quote_data['quote'],
                'urls': set(quote_data['urls'])
            }

DOCS = {
    1: "The quick brown fox jumps over the lazy dog",
    2: "The lazy dog is sleeping",
    3: "The fox is quick and clever"
}

HTML_WEIGHTS = {
    "title": 5,
    "heading": 4,
    "bold": 2,
    "italic": 1.5,
    "anchor": 1.5,
    "text": 1
}