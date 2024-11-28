from bs4 import BeautifulSoup
import requests

class Product: 
    def __init__(self, title=None, price=None, description=None, delivery=None, location=None) -> None:
        self.title = title 
        self.price = price 
        self.description = description 
        self.delivery = delivery 
        self.location = location
        
    def display(self):
        print("title: ", self.title)
        print("price: ", self.price)

class WebScraper: 
    def __init__(self, search) -> None:
        self.search: str = search
        self.product = []
        self.url = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={search}"

    def scrape(self):
        response = requests.get(self.url)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        products = soup.find_all("div", class_="s-item__wrapper")
        
        print(products[0])

        temp = []
        for product in products:
            p = Product()
            p.title = product.find_all(class_="s-item__title")
            p.price = product.find_all(class_="s-item__price")

            temp.append(p)

        for t in temp:
            t.display()

scraper = WebScraper(search="boots")
scraper.scrape()