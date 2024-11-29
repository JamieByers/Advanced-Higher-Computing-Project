class Product: 
    def __init__(self, title=None, price=None, details=None, description=None, delivery=None) -> None:
        self.title: str = title 
        self.price: str = price
        self.int_price: int = 0 
        self.cheapest_price: float = 0.0
        self.dearest_price: float = 0.0
        self.details = details
        self.delivery = delivery
        
    def display(self):
        print("title: ", self.title)
        print("price: ", self.price)
        print("cheapest price: ", self.cheapest_price)
        print("dearest price: ", self.dearest_price)
        print("delivery: ", self.delivery)