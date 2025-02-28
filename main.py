import time 
# Import my web scraper
from web_scraper import WebScraper

# checks if inputted key is valid
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
limit = 5
scraper = WebScraper(search_input=search_input, limit=limit)

# Scrape the products
products = scraper.scrape(threading=True, caching=True)

print(f"Found {len(products)} Products")

# Decide between searching the products found or searching them
decision = str(input("Would you like to search or sort the products found: "))
decision = decision.strip().lower()

while decision not in ["search", "sort"]:
    decision = str(input("Would you like to search or sort the products found: "))

if decision == "search":
    key = str(input("What value would you like to search by (price by default): "))
    if not key:
        key = "title"

    while not check_valid_key(key):
        key = str(input("What would you like to search by (price by default): "))
        if not key:
            key = "price"

    target = str(input("What would you like to search for: "))

    product_index = scraper.search(target=target, key=key)
    print("product index: ", product_index)

    if product_index > -1 and product_index != None:
        product = products[product_index]

        print(f"Found product with value of {target} for {key}: \n")
        product.display()
    else:
        print("Product not found")

elif decision == "sort":
    key = str(input("What would you like to sort by (price by default): "))
    if not key:
        key = "price"

    while not check_valid_key(key):
        key = str(input("What would you like to sort by (price by default): "))
        if not key:
            key = "price"

    descending_or_ascending = str(input("Would you like to sort by ascending order or by descending order (descending by default): "))
    while descending_or_ascending not in ["ascending", "descending"] :
        descending_or_ascending = str(input("Would you like to sort by ascending order or by descending order (descending by default)"))

    if descending_or_ascending == "ascending" or descending_or_ascending == "": 
        sorted_products = scraper.ascending_sort(key)
    else: 
        sorted_products = scraper.descending_sort(key)

    if sorted_products:
        print(f"Heres the sorted product information sorted by {key}: \n")
        for sp in sorted_products:
            sp.minimal_display()
    else:
        print("No products to be sorted")


else:
    raise RuntimeError("Expected search or sort to be either search or sort, found: ", decision)
