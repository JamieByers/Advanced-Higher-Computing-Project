class Searcher:
    def __init__(self, products):
        self.products = products


    def search(self, target, value):
        left = 0 
        right = len(self.products)
        found = False

        while left <= right and not found:
            middle = (left + right) // 2

            if getattr(value, self.products[middle]) == target: 
                return middle
            elif getattr(value, self.products[middle]) < target: 
                left = middle + 1
            else:
                right = middle - 1 