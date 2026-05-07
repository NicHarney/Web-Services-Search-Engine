# Web Crawler and Search Engine
## Overview
This project crawls web pages from QuotesToScrape, extracts text content, builds an inverted index and retrieves documents to build a search engine in python.

## Features
The search engine supports:
- Web crawling using Requests and BeautifulSoup
- AND-based document retrieval
- TF-IDF page ranking
- Deduplication of quotes
- HTML feature weighting
- Positional indexing
- Proximity-based ranking boosts
- Stemming using PorterStemmer
- Inverted index storage
- Automated unit tests using pytest
## Project Structure
- data/
  - index.json
- src/
  -  __init.py
  -  crawler.py
  -  indexer.py
  -  main.py
  -  search.py
-  tests/
  - test_crawler.py
  - test_indexer.py
  - test_search.py
- pytest.ini
- README.md
- requirements.txt
## Installation and Setup
### 1. Clone the repository
`git clone https://github.com/NicHarney/Web-Services-Search-Engine/`

`cd 'Search Engine'`

### 2. Create a Virtual Environment
`python -m venv venv`

### 3. Activate the virtual environment
Windows:
`venv\Scripts\activate`

macOs/Linux:
`source venv/bin/activate`

### 4. Install dependencies
`pip install -r requirements.txt`

## Dependencies
Main dependencies:
- requests
- beautifulsoup4
- nltk
- pytest

All dependencies can be installed using:

`pip install -r requirements.txt` 

## Usage
**Need to be in repository root directory Search Engine/**
### Build Command
Crawls the website and creates the inverted index.

`python -m src.main build`
### Load Command
Loads the saved index from disk.

`python -m src.main load`
### Print Command
Display postings information for a term in the inverted index. Terms are automatically normalised and stemmed before lookup.

`python -m src.main print nonsense`
### Find Command
Finds documents containing all query terms and ranks them using TF-IDF and proximity boosting.

`python -m src.main find good friends`
## Search Features
### TF-IDF Ranking
Documents are ranked using TF-IDF scoring based on term frequency and inverse document frequency.

### Positional Indexing
Token positions are stored to support proximity boosting

### Proximity Boosting
Documents where query terms appear closer together receive higher ranking scores.

### Stemming
Words are normalised using PorterStemmer so that related forms such as "find" and "finding" match the same indexed term.
## Testing
**Need to be in root directory Search Engine/**.

**pytest.ini must be present in the directory**.

Run all tests using:

`pytest`

Test suite covers:
- Tokenisation
- Indexing
- Deduplication
- Positional indexing
- TF-IDF retrieval
- Proximity boosting
- Persistence (save/load)
- Stemming

## Future Improvements
Potential Enhancements:
- PageRank Integration
- Full phrase querying (limited in this project due to powershell command parsing)
- Fuzzy matching
- Boolean query parsing
- BM25 ranking
