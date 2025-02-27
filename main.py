import time 
# Import my web scraper
from web_scraper import WebScraper

def check_valid_key(key): 
    if key in ["title",
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
        return True
    else:
        return False

search_input = str(input("Input your search input for your product: "))

# Create instance of my web scraper
limit = -1
scraper = WebScraper(search_input=search_input, limit=limit)

# Scrape the products
products = scraper.scrape(threading=True, caching=True)

search_or_sort = str(input("Would you like to search or sort the products found: "))
search_or_sort = search_or_sort.strip().lower()

while search_or_sort not in ["search", "sort"]:
    search_or_sort = str(input("Would you like to search or sort the products found: "))

if search_or_sort == "search":
    key = str(input("What value would you like to search by (title by default): "))
    if not key:
        key = "title"

    while not check_valid_key(key):
        key = str(input("What would you like to search by (title by default): "))
        if not key:
            key = "title"

    target = str(input("What would you like to search for: "))

    product_index = scraper.search(target=target, key=key)
    print("product index: ", product_index)

    if product_index > -1 and product_index != None:
        product = products[product_index]

        print(f"Found product with value of {target} for {key}: \n")
        product.display()
    else:
        print("Product not found")

elif search_or_sort == "sort":
    key = str(input("What would you like to sort by (price by default): "))
    if not key:
        key = "price"

    while not check_valid_key(key):
        key = str(input("What would you like to sort by (price by default): "))
        if not key:
            key = "price"

    sorted_products = scraper.sort(key)
    if sorted_products:
        print(f"Heres your product information sorted by {key}")
        for sp in sorted_products:
            sp.minimal_display()
    else:
        print("No products to be sorted")


else:
    raise RuntimeError("Expected search_or_sort to be either search or sort, found: ", search_or_sort)
