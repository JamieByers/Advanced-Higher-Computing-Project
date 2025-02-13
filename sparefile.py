from web_scraper import WebScraper

ws = WebScraper(search="boots", limit=5)
ws.scrape(threading=False, caching=True)
