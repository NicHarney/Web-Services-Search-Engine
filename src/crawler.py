import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
class Crawler:
    # Crawler class to fetch web pages, extract text, and find next page links
    def __init__(self,base_url,indexer):
        self.base_url = base_url
        self.indexer = indexer
        self.visited = set()
    
    # main loop to crawl pages, extract text, add to indexer and find next page until no more pages or a visited page is encountered
    def crawl(self):
        queue = deque([self.base_url])

        while queue:
            url = queue.popleft()
            if url in self.visited:
                continue
            print(f"Crawling: {url}")
            self.visited.add(url)
            html = self.fetch_page(url)
            text = self.extract_text(html)
            self.indexer.add_document(url, text)
            next_page = self.get_next_page(html)
            # add next page
            if next_page:
                queue.append(next_page)
            
            # add tag links
            tag_links = self.get_tag_links(html)
            for tag_link in tag_links:
                if tag_link not in self.visited:
                    queue.append(tag_link)
    
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

        content = []
        
        # Extract text from all span elements with each class and assign weights based on the type of content
        quotes = soup.find_all('span', class_='text')

        for quote in quotes:
            text = quote.get_text()

            content.append({
                "quote": text,
                "features": [
                    {
                    'text': text,
                    'type': 'text'
                    }
                ]
            })
        return content

    
    
    # Find URL of the next page
    def get_next_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # look for 'next' link in the page and return its absolute URL
        next_link = soup.find('li', class_='next')
        if next_link:
            href = next_link.find('a')['href']
            return urljoin(self.base_url, href)
        return None

    def get_tag_links(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('a', class_='tag')
        tag_links = []
        for tag in tags:
            href = tag.get('href')
            if href:
                tag_links.append(urljoin(self.base_url, href))
        return tag_links