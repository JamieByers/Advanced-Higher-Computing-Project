# Import my web scraper
from web_scraper import WebScraper

# Create instance of my web scraper
scraper = WebScraper(search="boots")

# Scrape the products
products = scraper.scrape(limit=3)

