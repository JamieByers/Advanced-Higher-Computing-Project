from web_scraper import WebScraper

ws = WebScraper(search="boots", limit=-1)

for i in range(5):
    ws.fetch_urls()
