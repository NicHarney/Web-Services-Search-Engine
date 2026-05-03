import sys
from src.indexer import Indexer
from src.search import Search
from src.crawler import Crawler

INDEX_FILE = "data/index.json"
BASE_URL = "http://quotes.toscrape.com/"

def build():
    indexer = Indexer()
    crawler = Crawler(BASE_URL, indexer)
    crawler.crawl()
    indexer.save(INDEX_FILE)

    print(f"Indexed {indexer.total_documents} documents.")

def load():
    indexer = Indexer()
    indexer.load(INDEX_FILE)
    return indexer

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [build|search]")
        return

    command = sys.argv[1]

    if command == "build":
        build()
    elif command == "load":
        indexer = load()
        print(f"Loaded index with {indexer.total_documents} documents.")
     
    elif command == "print":
        if len(sys.argv) < 3:
            print("Usage: python main.py print [term]")
            return
        indexer = load()
        term = sys.argv[2]
        print(indexer.get_postings(term))
    elif command == "find":
        if len(sys.argv) < 3:
            print("Usage: python main.py find [query]")
            return
        indexer = load()
        search = Search(indexer)
        query = " ".join(sys.argv[2:])
        results = search.find(query)
        print(f"Documents matching '{query}': {results}")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()