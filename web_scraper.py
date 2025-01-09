class WebScraper: 
    def __init__(self, search) -> None:
        # Search acts as the input to search for on the ebay search bar 
        self.search: str = search
        # This is the url used to get the html from ebay 
        self.url = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={search}"
        self.products = []

    def scrape(self):
        from product import Product
        from bs4 import BeautifulSoup
        import requests

        # Send request for website html and store it as a string 
        response = requests.get(self.url)
        html = response.text

        # Parse the html 
        soup = BeautifulSoup(html, "html.parser")

        # Find all div's with the class s-itme__wrapper, this gets all of the products on the page 
        products = soup.find_all("div", class_="s-item__wrapper")
        
        # Loop through all of the products found and store the information of the products in a the Product Object 
        for product in products:
            p = Product()

            p.details = product.find_all(class_="s-item__details-section--primary")
            p.title = product.find_all(class_="s-item__title")[0].text.strip()
            price = product.find_all(class_="s-item__price")[0].text.strip()

            link = product.find_all(class_="s-item__link")
            if link:
                p.link = link[0].get("href")

            p.price = price
            price_split = price.split(" ")

            p.cheapest_price = float(price_split[0][1:-1])
            p.dearest_price = float(price_split[-1][1:-1])

            delivery = product.find_all(class_="s-item__delivery-options")
            if delivery and len(delivery) > 0: 
                delivery = delivery[0].text.strip()
            elif delivery:
                delivery = delivery.text.strip()
            else:
                delivery = None

            p.delivery = delivery

            self.products.append(p)

    # Function to display all of the product information 
    def display(self):
        for product in self.products:
            product.display()

        print("Number of Products found: ", len(self.products))

