import sys
from src.indexer import Indexer
from src.search import Search
from src.crawler import Crawler

INDEX_FILE = "data/index.json"
BASE_URL = "http://quotes.toscrape.com/"

# build index by crawling the website and saving the index to a file
def build():
    indexer = Indexer()
    crawler = Crawler(BASE_URL, indexer)
    crawler.crawl()
    indexer.save(INDEX_FILE)

    print(f"Indexed {indexer.total_documents} documents.")

# load index
def load():
    indexer = Indexer()
    indexer.load(INDEX_FILE)
    return indexer

# main loop to hand CLI commands
def main():
    
    # check enough arguments are provided, otherwise print usage instructions
    if len(sys.argv) < 2:
        print("Usage: python main.py [build|search]")
        return

    # log which feature is being used based on the command provided
    command = sys.argv[1]

    # execute the appropriate function based on the command, with error handling for unknown commands and missing arguments
    if command == "build":
        build()
    elif command == "load":
        indexer = load()
        print(f"Loaded index with {indexer.total_documents} documents.")
     
    # print the postings list for a given term, with error handling for missing term argument
    elif command == "print":
        if len(sys.argv) < 3:
            print("Usage: python main.py print [term]")
            return
        indexer = load()

        # allocate term argument
        term = indexer.tokenize(sys.argv[2])[0]
        print(indexer.get_postings(term))
    
    # execute a search query and print the matching documents, with error handling for missing query argument
    elif command == "find":
        if len(sys.argv) < 3:
            print("Usage: python main.py find [query]")
            return
        indexer = load()
        search = Search(indexer)

        # allocate query argument
        query = " ".join(sys.argv[2:])
        query = indexer.tokenize(query)[0]  # Tokenize the query
        results = search.find(query)
        print(f"Documents matching '{query}': {results}")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()