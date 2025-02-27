import json
from product import Product

class Project:
    def __init__(self):
        self.products = []

    def input_validate(self, input):
        input = input.strip()
        return input

    def get_products(self):
        with open("cargo-trousers-data.json", "r") as file:
            products = json.load(file)
            for p in products:
                print("P", p)
                new_product = Product()
                new_product.productify(p)
                self.products.append(new_product)

        print(self.products)

        # Advanced Higher Concept - Binary Search Algorithm
    def search(self, target: str, key="price"):
        left = 0
        right = len(self.products)-1
        target = target.strip().lower()

        while left <= right:
            middle = (left + right) // 2
            # get the current product using an inputted key e.g title and it would get the title value e.g Yellow Boots - this would be similar to Product.title, but this works with any key
            current_product = getattr(self.products[middle], key).strip().lower() if isinstance(getattr(self.products[middle], key), str) else getattr(self.products[middle], key)
            if current_product == target:
                print("Product found at index: "+middle)
                print("Product information: \n ", self.products[middle].display())
                return middle
            elif current_product < target:
                left = middle + 1
            else:
                right = middle - 1

        print("Product not found")
        return -1 

    # Advanced Higher Concept - Bubble Sort Algorithm
    def sort(self, key="price"):

        # print unsorted array
        print("Before: ")
        print([getattr(p, key) for p in self.products]) # print only the key value of the product e.g only the product prices 

        swapped = True
        n = len(self.products)
        while n > 1 and swapped == True: # Only sort if there are products to sort and if the array is not sorted 
            swapped = False
            for i in range(n-1):
                # Search by the key inputted using getattr: this is instead of self.products[i].key. This means I dont have to write multiple search algorithms
                if getattr(self.products[i], key) > getattr(self.products[i + 1], key):
                    self.products[i], self.products[i+1] = self.products[i+1], self.products[i]
                    swapped = True

            n -= 1

        # print sorted array
        print("After: ")
        print([getattr(p, key) for p in self.products])
        return self.products

p = Project()

p.get_products()
p.sort("price")