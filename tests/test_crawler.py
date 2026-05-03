from unittest.mock import patch
from src.crawler import Crawler
from src.indexer import Indexer

# Test extract text from HTML
def test_extract_text():
    html = '''
    <html>
        <body>
            <span class="text">Quote 1</span>
            <span class="text">Quote 2</span>
        </body>
    </html>
    '''
    # Create a Crawler instance with a dummy base URL and an Indexer instance
    crawler = Crawler("http://example.com", Indexer())
    text = crawler.extract_text(html)
    assert "Quote 1" in text
    assert "Quote 2" in text

# Test get next page URL from HTML
def test_next_page():
    html = '''
    <html>
        <body>
            <li class="next">
                <a href="/page2">Next</a>
            </li>
        </body>
    </html>
    '''
    # Create a Crawler instance with a dummy base URL and an Indexer instance
    crawler = Crawler("http://example.com", Indexer())
    next_page = crawler.get_next_page(html)
    assert next_page.endswith("/page2")
