# Advanced Higher Concept - Object Oriented Programming - Product Object
class Product:
    # This is the constructor function. This assigns the parameters of the constructor function to the instance variables.
    def __init__(
        self, title: str = "", price: float = 0.0, buyer_protection_price: float = 0.0, postage: float = 0.0, brand: str = "", colour: str = "", size: str = "", quality: str = "", condition: str = "", location: str = "", payment_options: str = "", views: int = 0, description: str = "", url: str = "", uploaded: str = "", search_input: str = "",
    ):
        self.title = title
        self.price = price
        self.buyer_protection_price = buyer_protection_price
        self.postage = postage
        self.brand = brand
        self.size = size
        self.quality = quality
        self.condition = condition
        self.location = location
        self.payment_options = payment_options
        self.views = views
        self.description = description
        self.url = url
        self.colour = colour
        self.uploaded = uploaded
        self.search_input = search_input

    # This function will display all of the information the Product object stores
    def display(self):
        print("Product Details:")
        print(f"Title: {self.title}")
        print(f"Price: £{self.price:.2f}")
        print(f"Buyer Protection Price: £{self.buyer_protection_price:.2f}")
        print(f"Postage: £{self.postage:.2f}")
        print(f"Brand: {self.brand}")
        print(f"Colour: {self.colour}")
        print(f"Size: {self.size}")
        print(f"Quality: {self.quality}")
        print(f"Condition: {self.condition}")
        print(f"Location: {self.location}")
        print(f"Payment Options: {self.payment_options}")
        print(f"Views: {self.views}")
        print(f"Description: {self.description}")
        print(f"Uploaded: {self.uploaded}")
        print(f"URL: {self.url}")
        print(f"Search input: {self.search_input}")
        print()
        print()

    # This function will display a small amount of the information the Product object stores
    def minimal_display(self):
        print(f"Title: {self.title}")
        print(f"Price: £{self.price:.2f}")
        print(f"URL: {self.url}")

    # This turns a hashmap (dictionary/dict) into a Product object
    def productify(self, dict):
        self.title = dict.get("title", self.title)
        self.price = float(dict.get("price", self.price))
        self.buyer_protection_price = float(dict.get("buyer_protection_price", self.buyer_protection_price))
        self.postage = float(dict.get("postage", self.postage))
        self.brand = dict.get("brand", self.brand)
        self.colour = dict.get("colour", self.colour)
        self.size = dict.get("size", self.size)
        self.quality = dict.get("quality", self.quality)
        self.condition = dict.get("condition", self.condition)
        self.location = dict.get("location", self.location)
        self.payment_options = dict.get("payment_options", self.payment_options)
        self.views = int(dict.get("views", self.views))
        self.description = dict.get("description", self.description)
        self.url = dict.get("url", self.url)
        self.uploaded = dict.get("uploaded", self.uploaded)
        self.search_input = dict.get("search_input", self.search_input)
