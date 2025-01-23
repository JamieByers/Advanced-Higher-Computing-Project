class Searcher:
    def __init__(self, products):
        self.products = products
        n = len(products)

        left = 0 
        right = len(products)
        found = False

        while left <= right and not found:
            pass