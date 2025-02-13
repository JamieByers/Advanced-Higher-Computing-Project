import json
from product import Product

def search(products, target, key="title"):
    left = 0
    right = len(products)-1
    found = False

    while left <= right and not found:
        middle = (left + right) // 2

        print("nor: ", products[middle].title)
        print("curr: ", getattr(products[middle], key))
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

products = [p.title for p in products]
print(len(products))
print(len(set(products)))

print(search(products, "New look mid calf length boots. Size 5"))