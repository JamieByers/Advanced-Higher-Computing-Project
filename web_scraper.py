class WebScraper: 
    def __init__(self, search) -> None:
        self.search: str = search
        self.products = []
        self.url = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={search}"

    def scrape(self):
        from product import Product
        from bs4 import BeautifulSoup
        import requests

        response = requests.get(self.url)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        products = soup.find_all("div", class_="s-item__wrapper")
        

        temp = []
        for product in products:
            p = Product()
            p.details = product.find_all(class_="s-item__details-section--primary")
            
            p.title = product.find_all(class_="s-item__title")[0].text.strip()

            price = product.find_all(class_="s-item__price")[0].text.strip()

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

        for t in temp:
            t.display()

    def display(self):
        for product in self.products:
            product.display()

        print("Number of Products found: ", len(self.products))

