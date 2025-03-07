from db import Database
import json
from product import Product

def add_all_test():
    db = Database()
    db.initialise()
    with open("toy-data.json") as file:
        products = json.load(file)
        db.insert_products_to_db(products)

def add_individual():
    product = {
        "title": "Fruit pumps",
        "price": 2.0,
        "buyer_protection_price": 2.8,
        "postage": 2.29,
        "brand": "Primark",
        "size": "5",
        "quality": "Very good",
        "condition": "Very good",
        "location": "",
        "payment_options": "",
        "views": "9",
        "description": "Worn once small mark on toe",
        "url": "https://www.vinted.co.uk/items/5925263370-fruit-pumps?referrer=catalog",
        "colour": "White",
        "uploaded": "13 hours ago",
        "search_input": "shoes"
    }
    db = Database()
    db.initialise()
    db.insert_product(product)
