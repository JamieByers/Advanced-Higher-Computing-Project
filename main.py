# Import my web scraper
from web_scraper import WebScraper
# Import my database object which controls the access and retrival of product information in the database
from db import Database
# Import the searching and sorting functionalities
from search import *
from sort import ascending_sort, descending_sort
# Import the product object to allow type definition
from product import Product

# gets existing products from the database
def get() -> list:
    # set up database
    db = Database() # create instance of Database object

    # prompt user for search input of product to get from the database
    search_input = str(input("Input product search input: "))
    # input validate the search input by removing trailing spaces and upper case letters
    search_input = search_input.lower().strip()

    # get all of the products from the database that match the search input
    products: list[Product] = db.get_products_by_search_input(search_input)
    # display all of the products
    print("Products found: \n")
    for product in products:
        product.display()

    return products # return the products from the database

# scrapes new product data
def scrape() -> list:
    # prompt the user for a product to search for
    search_input: str = str(input("Input your search input for your product: "))
    # input validate the search input by removing trailing spaces and upper case letters
    search_input = search_input.strip().lower()

    limit: int = 5 # this is the limt to how many products the scraper will scrape, acting as rate limiter
    scraper: WebScraper = WebScraper(search_input=search_input, limit=limit) # Create instance of my web scraper

    # Scrape the products and store them in an array or objects
    products: list[Product] = scraper.decided_scrape(threading=True, caching=True)

    print(f"Found {len(products)} Products")

    return products

# checks if inputted key is valid
def check_valid_key(key: str) -> bool:
    # checks if the inputted key matches any of the available search or sort parameters
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

def handle_sort(products: list):
    # get the key the sorting function will sort by from the user
    key = str(input("What would you like to sort by (price by default): "))

    # set a default value for key if there is no input
    if not key:
        key = "price"

    # check if the products can be sorted by inputted key, if not input validate
    while not check_valid_key(key):
        key = str(input("What would you like to sort by (price by default): "))
        if not key:
            key = "price"

    # prompt the user to choose between sorting by ascending order or by descending order
    descending_or_ascending = input("Would you like to sort by ascending order or by descending order (ascending by default): ")

    # create default / fallback decision
    if descending_or_ascending == "":
        descending_or_ascending = "ascending"

    # input validate decision to ensure the decision is either ascending or descending
    while descending_or_ascending not in ["ascending", "descending"] :
        descending_or_ascending = str(input("Would you like to sort by ascending order or by descending order (ascending by default): "))

    # display array before sorting
    p = [getattr(p, key) for p in products]
    print("Before sorting: ", p)

    # sort by inputted decision, either ascending or descending
    if descending_or_ascending == "ascending":
        sorted_products = ascending_sort(products, key)
    else:
        sorted_products = descending_sort(products, key)

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

def handle_search(products: list):
    # get the key the searching function will search by from the user
    key = str(input("What value would you like to search by (price by default): "))
    # create default / fallback key
    if not key:
        key = "title"

    # check if the products can be searched by inputted key, if not input validate
    while not check_valid_key(key):
        # get the key the searching function will search by from the user
        key = str(input("What would you like to search by (price by default): "))
        # create default / fallback key
        if not key:
            key = "price" # default to price

    # this is the value that the search function is looking for
    target: str = str(input("What would you like to search for: "))

    # this is the index that the match product was found at, if not product was found the index will be -1
    product_index: int = search(products, target=target, key=key)

    # if the product is found display it
    if product_index > -1 and product_index != None:
        # set product to the found product
        product = products[product_index] # get the found product by using the product's index

        print(f"Found product with value of {target} for {key}: \n")
        product.display()
    else:
        print("Product not found")

# ---------------------------------------- MAIN PROGRAM ----------------------------------------------

# choose between scraping new products and getting existing ones from the database
options: list[str] = ["get", "scrape"]
# prompt the user to decide between scraping or sorting
main_decision: str = str(input("What would you like to do (options: get existing products: get, scrape new products: scrape): "))
# input validate the search input by removing trailing spaces and upper case letters
main_decision: str = main_decision.lower().strip()

# input validate the decision between scraping or getting
while main_decision not in options:
    # prompt the user to decide between scraping or sorting
    main_decision: str = str(input("What would you like to do (options: get existing products: get, scrape new products: scrape): "))
    # input validate the search input by removing trailing spaces and upper case letters
    main_decision: str = main_decision.lower().strip()

products = [] # create array for the products to be stored in
match main_decision: # matches the main decision to one of the possible decisions
    case "get":
        products: list = get() # gets products from the database and stores them in an array of objects
    case 'scrape':
        products: list = scrape() # scrapes products from the website and stores them in an array of objects

# Decide between searching the products found or searching them
decision: str = str(input("Would you like to search or sort the products found: "))
# input validate the decision by removing trailing spaces and upper case letters
decision: str = decision.strip().lower()

# input validate the decision
while decision not in ["search", "sort"]:
    decision = str(input("Would you like to search or sort the products found: "))

# search the products
if decision == "search":
    handle_search(products)

# sort the products
elif decision == "sort":
    handle_sort(products)

else:
    raise RuntimeError("Expected search or sort to be either search or sort, found: ", decision)
