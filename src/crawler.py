import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
class Crawler:
    # Crawler class to fetch web pages, extract text, and find next page links
    def __init__(self,base_url,indexer):
        self.base_url = base_url
        self.indexer = indexer
        self.visited = set()
    
    # main loop to crawl pages, extract text, add to indexer and find next page until no more pages or a visited page is encountered
    def crawl(self):
        url = self.base_url

        while url:
            if url in self.visited:
                break

            self.visited.add(url)
            html = self.fetch_page(url)
            text = self.extract_text(html)
            self.indexer.add_document(url, text)
            url = self.get_next_page(html)
    
    # Fetch a web page and return its HTML content, with error handling and a politeness delay
    def fetch_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            time.sleep(6)  # Politeness delay
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""
    
    # extract text from HTML
    def extract_text(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract text from all span elements with class 'text'
        quotes = soup.find_all('span', class_='text')

        # Combine the text from all quotes into a single string
        text_data = []
        for quote in quotes:
            text_data.append(quote.get_text())
        return ' '.join(text_data)
    
    # Find URL of the next page
    def get_next_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # look for 'next' link in the page and return its absolute URL
        next_link = soup.find('li', class_='next')
        if next_link:
            href = next_link.find('a')['href']
            return urljoin(self.base_url, href)
        return None