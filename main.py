# Import my web scraper
from web_scraper import WebScraper

# input = str(input("What product would you like to search for: "))

# Create instance of my web scraper
scraper = WebScraper(search="boots")

# search_or_sort = str(input("Would you like to search or sort the products found: "))
# search_or_sort = search_or_sort.strip()
# search_or_sort = search_or_sort.lower()
# while search_or_sort not in ["search", "sort"]: 
#     search_or_sort = str(input("Would you like to search or sort the products found: "))




# Scrape the products
products = scraper.scrape(limit=3)

