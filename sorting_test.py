import json
from product import Product
import time

# Advanced Higher Concept - Bubble Sort Algorithm
def sort(products, key="price"):
    n = len(products)
    while n > 1: # Only sort if there are products to sort
        swapped = False
        for i in range(n-1):
            # Search by the key inputted using getattr: this is instead of products[i].key. This means I dont have to write multiple search algorithms
            if getattr(products[i], key) > getattr(products[i + 1], key):
                products[i], products[i+1] = products[i+1], products[i]
                swapped = True

        if not swapped:
            break

        n -= 1


products = []
with open("boots-data.json", "r") as file:
    js = json.loads(file.read())
    for p in js:
        product = Product()
        product.productify(p)

        products.append(product)

sort(products)

for param in ["title",
            "price",
            "buyer_protection_price",
            "postage",
            "brand",
            "size",
            "quality",
            "condition",
            "location",
            "payment_options",
            "views",
            "description",
            "url",
            "colour",
            "uploaded",]:
    print([getattr(product, param) for product in products ])
    print()
    sort(products, key=param)
    new_ps = [getattr(product, param) for product in products ]
    print(new_ps)
    if new_ps == sorted(new_ps):
        print("Sorted: True")
    else:
        print("Sorted: False")

    print()
    
