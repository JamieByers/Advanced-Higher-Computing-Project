import time 

# Import my web scraper
from web_scraper import WebScraper

start = time.time()

# Create instance of my web scraper
limit = 25

scraper = WebScraper(search="boots", limit=limit)

# Scrape the products
products = scraper.scrape(threading=True, caching=True)

end = time.time()

time = end - start

print(f"Webscraper took {time} for {len(products)} items")


