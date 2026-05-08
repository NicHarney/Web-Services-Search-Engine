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
    try:
        indexer.load(INDEX_FILE)
    except FileNotFoundError:
        print("No index file found, please run the build command first")
        return None
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
        if indexer is None:
            return
        print(f"Loaded index with {indexer.total_documents} documents.")
     
    # print the postings list for a given term, with error handling for missing term argument
    elif command == "print":
        if len(sys.argv) < 3:
            print("Usage: python main.py print [term]")
            return
        indexer = load()

        if indexer is None:
            return
        # allocate term argument
        term = indexer.tokenize(sys.argv[2])
        if not term:
            print("Term must contain at least one valid token.")
            return
        term = term[0]  # Use the first token from the term argument
        print(indexer.get_postings(term))
    
    # execute a search query and print the matching documents, with error handling for missing query argument
    elif command == "find":
        if len(sys.argv) < 3:
            print("Usage: python main.py find [query]")
            return
        indexer = load()
        if indexer is None:
            return
        search = Search(indexer)

        # allocate query argument
        query = " ".join(sys.argv[2:])
        query = indexer.tokenize(query)
        if not query:
            print("Query must contain at least one valid token.")
            return
        query = query[0]  # Use the first token from the query argument
        results = search.find(query)
        print(f"Documents matching '{query}': {results}")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()