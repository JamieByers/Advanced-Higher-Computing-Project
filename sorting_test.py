import json
import unittest
from product import Product

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

class TestProductSorter(unittest.TestCase):
    def setUp(self):
        self.products = []
        with open("boots-data.json", "r") as file:
            data = json.load(file)
            for p in data:
                product = Product()
                product.productify(p)
                self.products.append(product)
    
    def test_sort_by_title(self):
        self._test_sorting("title")

    def test_sort_by_price(self):
        self._test_sorting("price")

    def test_sort_by_buyer_protection_price(self):
        self._test_sorting("buyer_protection_price")

    def test_sort_by_postage(self):
        self._test_sorting("postage")

    def test_sort_by_brand(self):
        self._test_sorting("brand")

    def test_sort_by_size(self):
        self._test_sorting("size")

    def test_sort_by_quality(self):
        self._test_sorting("quality")

    def test_sort_by_condition(self):
        self._test_sorting("condition")

    def test_sort_by_location(self):
        self._test_sorting("location")

    def test_sort_by_payment_options(self):
        self._test_sorting("payment_options")

    def test_sort_by_views(self):
        self._test_sorting("views")

    def test_sort_by_description(self):
        self._test_sorting("description")

    def test_sort_by_url(self):
        self._test_sorting("url")

    def test_sort_by_colour(self):
        self._test_sorting("colour")

    def test_sort_by_uploaded(self):
        self._test_sorting("uploaded")

    def _test_sorting(self, key):
        products_copy = self.products.copy()
        sort(products_copy, key=key)
        sorted_values = [getattr(p, key) for p in products_copy]
        self.assertEqual(sorted_values, sorted(sorted_values), f"Sorting failed for key: {key}")

if __name__ == "__main__":
    unittest.main()
