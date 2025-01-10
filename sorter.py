class Sorter: 
    def __init__(self, ):
        self.products = []

    def sort(self, key):
        n = len(self.products)
        swapped = True
        while swapped and n >= 0:
            swapped = False 
            for i in range(n-1):
                # Search by the key inputted using getattr: this is instead of self.products[i].key. This means I dont have to write multiple search algorithms 
                if getattr(self.products[i], key) > getattr(self.products[i + 1], key):
                    self.products[i], self.products[i+1] = self.products[i+1], self.products[i]
            n -= 1