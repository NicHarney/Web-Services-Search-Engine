import math
class Search:

    def __init__(self, indexer):
        self.indexer = indexer

    # Find documents that match the query terms using an AND search strategy
    def find(self, query):
        query_terms = self.indexer.tokenize(query)
        if not query_terms:
            return []
        
        # implement idf ranking
        doc_scores = {}
        N = self.indexer.total_documents
        for term in query_terms:
            postings = self.indexer.get_postings(term)
            df = len(postings)

            if df == 0:
                continue
            idf = math.log((N + 1) / (df + 1)) + 1 # Adding 1 to avoid division by zero and to smooth idf

            for doc, tf in postings.items():
                tf = tf['score']  # Get the term frequency score from the postings
                score = tf * idf
                if doc not in doc_scores:
                    doc_scores[doc] = 0
                doc_scores[doc] += score
        # sort documents by score in descending order
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        result_urls = []
        seen = set()
        for doc, score in ranked_docs:
            urls = self.indexer.quotes[doc]['urls']
            for url in urls:
                if url not in seen:
                    result_urls.append(url)
                    seen.add(url)
        return result_urls
    
    # print documents containing a certain word along with their frequencies
    def print_word(self,word):
        postings = self.indexer.get_postings(word)
        if not postings:
            print(f"No documents contain the word '{word}'.")
            return
        print(f"Documents containing the word '{word}':")
        for doc_id, freq in postings.items():
            print(f"Document ID: {doc_id}, Frequency: {freq}")

