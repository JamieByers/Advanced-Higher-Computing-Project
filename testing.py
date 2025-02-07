from web_scraper import WebScraper

wbs = WebScraper(search="Boots", limit=5)

for i in range(5):
    try:
        urls = wbs.fetch_urls()
        if urls:
            print("Successful!!!")
        else:
            print("Unsuccessful :(")
    except:
        
        print("Unsuccessful :(")