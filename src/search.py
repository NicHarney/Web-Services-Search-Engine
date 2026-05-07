import math
class Search:

    def __init__(self, indexer):
        self.indexer = indexer

    # Find documents that match the query terms using an AND search strategy
    def find(self, query):

       
        query = query.strip()
      
        # check if the query is a phrase search (enclosed in quotes) and handle it separately
        if self._is_phrase_query(query):
            phrase = query[1:-1]
            
            return self.phrase_search(phrase)

        # tokenize the query
        query_terms = self.indexer.tokenize(query)
        
        if not query_terms:
            return []

        # retrieve postings lists for each query term and find the intersection of documents that contain all query terms
        postings_lists = [self.indexer.get_postings(term) for term in query_terms]
        if any(len(p) == 0 for p in postings_lists):
            return []
        
        # find documents that contain all query terms
        common_docs = set(postings_lists[0].keys())
        for postings in postings_lists[1:]:
            # intersect the sets of documents for each term to find common documents that contain all query terms
            common_docs &= set(postings.keys())
        
        # implement idf ranking
        doc_scores = {}
        N = self.indexer.total_documents
        for term in query_terms:
          
            postings = self.indexer.get_postings(term)
            df = len(postings)

            if df == 0:
                continue
            # Adding 1 to avoid division by zero and to smooth idf
            idf = math.log((N + 1) / (df + 1)) + 1 

            for doc_id in common_docs:
                # Get the term frequency score from the postings
                tf = postings[doc_id]['score'] 
                score = tf * idf

                # accumulate scores for each document
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = 0
                doc_scores[doc_id] += score
            # proximity boost
            if len(query_terms) >= 2:
                for doc_id in common_docs:
                    proximity_boost = 0

                    # calculate proximity boost based on the minimum distance between query terms in the document
                    for i in range(len(query_terms) - 1):
                        term1 = query_terms[i]
                        term2 = query_terms[i + 1]
                        postings1 = self.indexer.get_postings(term1)
                        postings2 = self.indexer.get_postings(term2)
                        positions1 = postings1[doc_id]['positions']
                        positions2 = postings2[doc_id]['positions']
                        
                        min_dist = self.minimum_distance(positions1, positions2)
                        # Add 1 to avoid division by zero
                        proximity_boost += 1 / (min_dist + 1)
                    
                    # Proximity boost weight
                    doc_scores[doc_id] += proximity_boost * 2 


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

    # helper function to check if a query is a phrase search (enclosed in quotes)
    def _is_phrase_query(self, query):
        return len(query) >= 2 and query[0] == '"' and query[-1] == '"'


    # perform a phrase search by checking if the exact sequence of words appears in the same order in the documents
    def phrase_search(self, phrase):

        words = self.indexer.tokenize(phrase)
        if not words:
            return []

        # retrieve list for each word in the phrase
        postings_lists = [self.indexer.get_postings(word) for word in words]

        # if any word in the phrase does not appear in any document, return an empty list
        if any(len(p) == 0 for p in postings_lists):
            return []
        
        # find documents that contain all words in the phrase by intersecting the sets of documents for each word
        common_docs = set(postings_lists[0].keys())

        for postings in postings_lists[1:]:
            common_docs &= set(postings.keys())

        matching_docs = []

        # check if the words in the phrase appear in the correct order and positions in the documents
        for doc_id in common_docs:
            positions_lists = [
                postings[doc_id]['positions'] for postings in postings_lists
            ]

            first_word_positions = positions_lists[0]

            # check if the subsequent words in the phrase appear in the correct positions relative to the first word
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

    # convert document IDS to urls for output
    def _docs_to_urls(self, doc_ids):
        return [self.indexer.documents[doc_id]['url'] for doc_id in doc_ids]

    # calculate minimum distance between two positions lists for proximity ranking
    def minimum_distance(self, positions1, positions2):
        i, j = 0, 0
        min_dist = float('inf')
        # use a two-pointer technique to find the minimum distance between any two positions in the lists
        while i < len(positions1) and j < len(positions2):
            min_dist = min(min_dist, abs(positions1[i] - positions2[j]))
            if positions1[i] < positions2[j]:
                i += 1
            else:
                j += 1
        return min_dist