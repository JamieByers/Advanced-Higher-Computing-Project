from product import Product
import json
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

hash = {
        "title": "black asos boots",
        "price": 5.0,
        "buyer_protection_price": 5.95,
        "postage": 2.49,
        "brand": "ASOS",
        "size": "7",
        "quality": "Good",
        "condition": "Good",
        "location": "",
        "payment_options": "Credit card",
        "views": "61",
        "description": "worn a few times",
        "url": "https://www.vinted.co.uk/items/5812662581-black-asos-boots?referrer=catalog",
        "colour": "Black",
        "uploaded": "13 hours ago"
}

def search(products, target, key="price"):
    left = 0
    right = len(products)-1
    found = False

    while left <= right and not found:
        middle = (left + right) // 2

        if getattr(products[middle], key) == target:
            found = True
            return middle
        elif getattr(products[middle], key) < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1 


products = []
with open("boots-data.json", "r") as file:
    js = json.loads(file.read())
    for p in js:
        product = Product()
        product.productify(p)

        products.append(product)

sort(products)

counter = 0
for (param, value) in hash.items():
    print(f"Looking for {param} with value of '{value}'")
    
    sort(products, key=param)
    index = search(products, target=value, key=param)

    products[index].display()

    if getattr(products[index], param) == value:
        print("TEST CASE PASSED")
        counter += 1
    else:
        print("TEST CASE FAILED")

    print()

print(f"Test cases passed: {counter}/{len(hash)}")