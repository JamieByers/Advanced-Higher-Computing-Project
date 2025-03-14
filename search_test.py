from db import Database
from search import search

db = Database()
db.initialise()
products = db.get_products_by_search_input("toy")

looking_for = products[-1].__dict__

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
    
    found = search(products, looking_for[param], param)
    
    if found >= 0: 
        print("FOUND FOR PARAM", param, "AT", found)
    else: 
        print("NOT FOUND FOR PARAM", param)


