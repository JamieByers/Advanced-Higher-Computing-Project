class WebScraper:
    def __init__(self, search) -> None:
        # Search acts as the input to search for on the ebay search bar
        self.search: str = search
        # This is the url used to get the html from ebay
        self.url = f"https://www.vinted.co.uk/catalog?search_text={search}"
        self.products = []

    def scrape(self):
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(self.url)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        feed_grid = soup.find_all("div", class_="feed-grid__item-content")

        print("feed_grid", feed_grid)

        if feed_grid:
            products = feed_grid.find_all("div", class_="grid-item")
            print(products)
        else:
            print("ERROR NO FEED GRID")



    # Function to display all of the product information
    def display(self):
        for product in self.products:
            product.display()

        print("Number of Products found: ", len(self.products))

