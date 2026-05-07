import math
class Search:

    def __init__(self, indexer):
        self.indexer = indexer

    # Find documents that match the query terms using an AND search strategy
    def find(self, query):

       
        query = query.strip()
      
        if self._is_phrase_query(query):
            phrase = query[1:-1]
            
            return self.phrase_search(phrase)

        query_terms = self.indexer.tokenize(query)
        
        if not query_terms:
            return []

        postings_lists = [self.indexer.get_postings(term) for term in query_terms]
        if any(len(p) == 0 for p in postings_lists):
            return []
        
        common_docs = set(postings_lists[0].keys())
        for postings in postings_lists[1:]:
            common_docs &= set(postings.keys())
        
        # implement idf ranking
        doc_scores = {}
        N = self.indexer.total_documents
        for term in query_terms:
          
            postings = self.indexer.get_postings(term)
            df = len(postings)

            if df == 0:
                continue
            idf = math.log((N + 1) / (df + 1)) + 1 # Adding 1 to avoid division by zero and to smooth idf

            for doc_id in common_docs:
                tf = postings[doc_id]['score'] # Get the term frequency score from the postings
                score = tf * idf
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = 0
                doc_scores[doc_id] += score
            # proximity boost
            if len(query_terms) >= 2:
                for doc_id in common_docs:
                    proximity_boost = 0

                    for i in range(len(query_terms) - 1):
                        term1 = query_terms[i]
                        term2 = query_terms[i + 1]
                        postings1 = self.indexer.get_postings(term1)
                        postings2 = self.indexer.get_postings(term2)
                        positions1 = postings1[doc_id]['positions']
                        positions2 = postings2[doc_id]['positions']
                        
                        min_dist = self.minimum_distance(positions1, positions2)
                        proximity_boost += 1 / (min_dist + 1) # Add 1 to avoid division by zero
                    doc_scores[doc_id] += proximity_boost * 2 # Proximity boost weight


        # sort documents by score in descending order
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        
     
        return self._docs_to_urls([doc_id for doc_id, score in ranked_docs])
    
    # print documents containing a certain word along with their frequencies
    def print_word(self,word):
        postings = self.indexer.get_postings(word)
        if not postings:
            print(f"No documents contain the word '{word}'.")
            return
        print(f"Documents containing the word '{word}':")
        for doc_id, freq in postings.items():
            print(f"Document ID: {doc_id}, Frequency: {freq}")

    def _is_phrase_query(self, query):
        return len(query) >= 2 and query[0] == '"' and query[-1] == '"'


    def phrase_search(self, phrase):

        words = self.indexer.tokenize(phrase)
        if not words:
            return []

        postings_lists = [self.indexer.get_postings(word) for word in words]

        if any(len(p) == 0 for p in postings_lists):
            return []
        
        common_docs = set(postings_lists[0].keys())

        for postings in postings_lists[1:]:
            common_docs &= set(postings.keys())

        matching_docs = []

        for doc_id in common_docs:
            positions_lists = [
                postings[doc_id]['positions'] for postings in postings_lists
            ]

            first_word_positions = positions_lists[0]
            for pos in first_word_positions:
                phrase_match = True

                # Check if the subsequent words appear in the correct positions
                for i in range(1, len(positions_lists)):
                    if (pos + i) not in positions_lists[i]:
                        phrase_match = False
                        break
                if phrase_match:
                    matching_docs.append(doc_id)
                    break
        return self._docs_to_urls(matching_docs)

    def _docs_to_urls(self, doc_ids):
        return [self.indexer.documents[doc_id]['url'] for doc_id in doc_ids]

    def minimum_distance(self, positions1, positions2):
        i, j = 0, 0
        min_dist = float('inf')
        while i < len(positions1) and j < len(positions2):
            min_dist = min(min_dist, abs(positions1[i] - positions2[j]))
            if positions1[i] < positions2[j]:
                i += 1
            else:
                j += 1
        return min_dist