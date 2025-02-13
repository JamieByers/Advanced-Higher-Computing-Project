import time 

# Import my web scraper
from web_scraper import WebScraper

start = time.time()

# Create instance of my web scraper
limit = 5
scraper = WebScraper(search="sandals", limit=limit)


# Scrape the products
products = scraper.scrape()

end = time.time()

time = end - start

print(f"Webscraper took {time} for {len(products)} items")

for _ in range(5):
    print()

print([p.price for p in scraper.products])

scraper.sort()

print([p.price for p in scraper.products])
