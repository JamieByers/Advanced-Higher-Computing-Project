import time 

# Import my web scraper
from web_scraper import WebScraper

start = time.time()

# Create instance of my web scraper
limit = 2
scraper = WebScraper(search="boots", limit=5)


# Scrape the products
products = scraper.scrape()

end = time.time()

time = end - start

print(f"Webscraper took {time} for {len(products)} items")