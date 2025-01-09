class Sorter: 
    def __init__(self, ):
        self.products = []

    def sort(self):
        n = len(self.products)
        swapped = True
        while swapped and n >= 0:
            swapped = False 
            for i in range(n-1):
                if self.products[i].int_price > self.products[i+1].int_price:
                    self.products[i], self.products[i+1] = self.products[i+1], self.products[i]
            n -= 1