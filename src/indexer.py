import json
import re
import os
from nltk.stem import PorterStemmer
#  Inverted Indexer Implementation
class Indexer:

    # Initialize the indexer with an empty index and document count
    def __init__(self):
        self.index = {}
        self.total_documents = 0

        self.quote_map = {}
        self.quotes = {}
        self.next_doc_id = 0
        self.next_quote_id = 0
        self.documents = {}

        self.stemmer = PorterStemmer()

    # get or create unique ID for a quote to avoid duplication in the index and store the quote text
    def _get_or_create_quote_id(self, quote):
        if quote not in self.quote_map:
            quote_id = str(self.next_quote_id)
            self.quote_map[quote] = quote_id
            self.quotes[quote_id] = quote
            self.next_quote_id += 1
            return quote_id
        return self.quote_map[quote]
    
    # add a document to the indexer and update the index and document count
    def add_document(self, url, content):
        url = str(url)
        doc_id = str(self.next_doc_id)
        self.next_doc_id += 1
        self.documents[doc_id] = {
            "url": url,
            "quotes": []
        }

        # Process each quote and its features, tokenize the text, and update the index with term frequencies and positions
        current_position = 0
        for item in content:

            # Get or create a unique quote ID for the quote text and store it in the document's quote list
           quote_text = item['quote']
           quote_id = self._get_or_create_quote_id(quote_text)

           self.documents[doc_id]["quotes"].append(quote_id)

        
           # process each feature and tokenise, then apply weighting
           for feature in item['features']:
                text = feature['text']
                feature_type = feature['type']

                # weighting based on HTML element type
                weight = HTML_WEIGHTS.get(feature_type, 1)
                words = self.tokenize(text)

                # update index with term frequencies and positions for each word in the feature text
                for word in words:

                    # if if the word is not in the index, add it
                    if word not in self.index:
                        self.index[word] = {}
                    

                    # if the document is not in the postings list for the word, add it with initial score and positions
                    if doc_id not in self.index[word]:
                        self.index[word][doc_id] = {
                            "score": 0,
                            "positions": []
                        }
                    
                    # update the score and positions for the word in the document based on the feature weight
                    self.index[word][doc_id]['score'] += weight
                    self.index[word][doc_id]['positions'].append(current_position)
                    current_position += 1
        self.total_documents += 1
    # tokenize text to lowercase words and remove punctuation
    def tokenize(self, text):
        # case insensitivity
        text = text.lower()

        # use regex to find words
        words = re.findall(
            r'\b[a-zA-Z0-9]+\b', text
        )  
        
        stemmed_words = []

        # remove stopwords and apply stemming to each word, then return the list of processed words
        for word in words:

            if word in STOPWORDS:
                continue
            stemmed = self.stemmer.stem(word)
            stemmed_words.append(stemmed)
        return stemmed_words

    # Retrieve the postings list for a given term, returning an empty dictionary if the term is not found
    def get_postings(self, term):
        word = term.lower()
        return self.index.get(word, {})
    
    # Save the index and document count to a JSON file
    def save(self, filepath):
        # create path if not exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:

            json.dump({
                'index': self.index,
                'documents': self.documents,
                'quotes': self.quotes,
                'quote_map': self.quote_map,
                'total_documents': self.total_documents,
                'next_doc_id': self.next_doc_id,
                'next_quote_id': self.next_quote_id

            }, f)
    # Load the index and document count from a JSON file
    def load(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.index = data['index']
        self.quote_map = data['quote_map']
        self.total_documents = data['total_documents']
        self.next_doc_id = data['next_doc_id']
        self.next_quote_id = data['next_quote_id']
        self.quotes = data['quotes']
        self.documents = data['documents']
     
# HTML element weights for scoring
HTML_WEIGHTS = {
    "title": 5,
    "heading": 4,
    "bold": 2,
    "italic": 1.5,
    "anchor": 1.5,
    "text": 1
}

# Common stopwords to exclude from indexing
STOPWORDS = {
    "the", "is", "and", "a", "an", "in", "on", "at", "to", "for", "with",
    "by", "of", "that", "this", "it", "as", "are", "was", "were",
    "be", "from", "or", "which"
}