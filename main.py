import time 
# Import my web scraper
from web_scraper import WebScraper
from db import Database
from search import *
from sort import ascending_sort, descending_sort

def get() -> list:
    # set up database
    db = Database()
    db.initialise()

    search_input = str(input("Input product search input: "))
    search_input = search_input.lower().strip()

    products = db.get_products_by_search_input(search_input)
    print("Products found: \n")
    for product in products:
        product.display()

    return products

def scrape() -> list:
    
    search_input = str(input("Input your search input for your product: "))

    # Create instance of my web scraper
    limit = 5
    scraper = WebScraper(search_input=search_input, limit=limit)

    # Scrape the products
    products = scraper.scrape(threading=True, caching=True)

    print(f"Found {len(products)} Products")

    return products

# checks if inputted key is valid
def check_valid_key(key) -> bool: 
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


def handle_sort(products):
    key = str(input("What would you like to sort by (price by default): "))
    if not key:
        key = "price"

    # check if the products can be sorted by inputted key, if not input validate
    while not check_valid_key(key):
        key = str(input("What would you like to sort by (price by default): "))
        if not key:
            key = "price"

    # input validate decision to sort either ascending or descending 
    descending_or_ascending = str(input("Would you like to sort by ascending order or by descending order (descending by default): "))

    if descending_or_ascending == "": 
        descending_or_ascending = "ascending"

    while descending_or_ascending not in ["ascending", "descending"] :
        descending_or_ascending = str(input("Would you like to sort by ascending order or by descending order (descending by default): "))

    # sort by inputted decision 
    if descending_or_ascending == "ascending":
        sorted_products = ascending_sort(products, key)
    else: 
        sorted_products = descending_sort(products, key)

    # show array before sorting 
    p = [getattr(p, key) for p in products]
    print("Before sorting: ", p)

    # if there are any sorted products display them 
    if sorted_products:
        # show array after sorting 
        ps = [getattr(p, key) for p in sorted_products]
        print("After sorting: ", ps)

        print(f"Heres the sorted product information sorted by {key}: \n")
        for sp in sorted_products:
            sp.minimal_display()
    else:
        print("No products to be sorted")

def handle_search(products):
    key = str(input("What value would you like to search by (price by default): "))
    if not key:
        key = "title"


    # check if the products can be sorted by inputted key, if not input validate
    while not check_valid_key(key):
        key = str(input("What would you like to search by (price by default): "))
        if not key:
            key = "price" # default to price

    target = str(input("What would you like to search for: "))

    products = ascending_sort(products, key)
    product_index = search(products, target=target, key=key)

    # if the product is found display it 
    if product_index > -1 and product_index != None:
        product = products[product_index]

        print(f"Found product with value of {target} for {key}: \n")
        product.display()
    else:
        print("Product not found")


options = ["get", "scrape"]
main_decision = str(input("What would you like to do (options: get existing products: get, scrape new products: scrape): "))
main_decision= main_decision.lower().strip()

while main_decision not in options:
    main_decision = str(input("What would you like to do (options: get existing products: get, scrape new products: scrape): "))
    main_decision= main_decision.lower().strip()

products = []
match main_decision:
    case "get":
        products = get()
    case 'scrape':
        products = scrape()

# Decide between searching the products found or searching them
decision = str(input("Would you like to search or sort the products found: "))
decision = decision.strip().lower()

# input validate the decision 
while decision not in ["search", "sort"]:
    decision = str(input("Would you like to search or sort the products found: "))

if decision == "search":
    handle_search(products)

elif decision == "sort":
    handle_sort(products)

else:
    raise RuntimeError("Expected search or sort to be either search or sort, found: ", decision)
