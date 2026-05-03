class Search:

    def __init__(self, indexer):
        self.indexer = indexer

    # Find documents that match the query terms using an AND search strategy
    def find(self, query):
        query_terms = self.indexer.tokenize(query)
        if not query_terms:
            return []
        
        # Get postings for the first term
        first_term = query_terms[0]
        postings = self.indexer.get_postings(first_term)
        
        # If no postings for the first term, return empty result
        if not postings:
            return []
        
        # Initialize results with document IDs from the first term
        results = set(postings.keys())
        
        # Intersect with postings of subsequent terms
        for term in query_terms[1:]:
            term_postings = self.indexer.get_postings(term)
            if not term_postings:
                return []  # If any term has no postings, return empty result
            results.intersection_update(term_postings.keys())
        
        return list(results)
    
    # print documents containing a certain word along with their frequencies
    def print_word(self,word):
        postings = self.indexer.get_postings(word)
        if not postings:
            print(f"No documents contain the word '{word}'.")
            return
        print(f"Documents containing the word '{word}':")
        for doc_id, freq in postings.items():
            print(f"Document ID: {doc_id}, Frequency: {freq}")

