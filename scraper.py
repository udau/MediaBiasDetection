import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_fox_news(url):
    """
    Scrapes the full content of a Fox News article.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Fox News articles usually have content in div.article-body
        article_body = soup.find('div', class_='article-body')
        if not article_body:
            # Fallback for different layouts
            article_body = soup.find('article')
            
        if not article_body:
            logger.warning(f"Could not find article body for URL: {url}")
            return None
            
        # Extract paragraphs, excluding ads or related links if possible
        paragraphs = article_body.find_all('p')
        content = []
        for p in paragraphs:
            # Skip empty paragraphs or those that look like ads/links
            text = p.get_text(strip=True)
            if text and len(text) > 20: # Crude filter for meaningful content
                content.append(text)
        
        return "\n\n".join(content)
        
    except Exception as e:
        logger.error(f"Error scraping Fox News article at {url}: {e}")
        return None

def scrape_article(url):
    """
    Main entry point for scraping articles from various sources.
    """
    if 'foxnews.com' in url:
        return scrape_fox_news(url)
    
    # Add more sources here as needed
    logger.info(f"No specific scraper implemented for: {url}")
    return None

if __name__ == "__main__":
    # Quick test
    test_url = "https://www.foxnews.com/opinion/one-month-at-war-with-iran-can-washington-define-victory"
    print(f"Scraping: {test_url}")
    content = scrape_article(test_url)
    if content:
        print("Scrape successful!")
        print(content[:500] + "...")
    else:
        print("Scrape failed.")
