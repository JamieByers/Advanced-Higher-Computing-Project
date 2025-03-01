import mysql.connector
import json
from product import Product

class Database:
    def __init__(self):
        self.cursor = None
        self.connection = None

    def initialise(self):
        db_config = {
            "host": "localhost",      
            "user": "jamie",           
            "password": "password", 
            "database": "products_database"
        }

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        self.connection = connection
        self.cursor = cursor

        return self.cursor
    
    def is_a_duplicate(self, product):
        search_input = product["search_input"]

        sql = "SELECT * FROM products WHERE search_input=%s"

        self.cursor.execute(sql, (search_input,))
        fetched_products = self.cursor.fetchall()

        url_column_index = 14
        
        for fetched_product in fetched_products:
            if fetched_product[url_column_index] == product["url"]:
                return True
        
        return False


    def insert_products_to_db(self, products):
        for product in products:
            self.insert_product(product)

        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def insert_product(self, product):
        if self.is_a_duplicate(product):
            print("Product is a duplicate")
            return 

        sql = """
        INSERT INTO products 
        (title, price, buyer_protection_price, postage, brand, colour, size, quality, `condition`, location, payment_options, views, description, url, uploaded, search_input) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        
        values = (
            product['title'],
            product['price'],
            product['buyer_protection_price'],
            product['postage'],
            product['brand'],
            product['colour'],
            product['size'],
            product['quality'],
            product['condition'],
            product['location'],
            product['payment_options'],
            product['views'],
            product['description'],
            product['url'],
            product['search_input']  
        )

        try:
            self.cursor.execute(sql, values)
            print("Product added successfully!")
        except mysql.connector.Error as err:
            print("Error:", err)

    def get_products_by_search_input(self, search_input):
        sql = "SELECT * FROM products WHERE search_input=%s"

        try:
            self.cursor.execute(sql, (search_input,))
            fetched_products = self.cursor.fetchall()

            column_names = [desc[0] for desc in self.cursor.description]
            products = []
            for fetched_product in fetched_products:
                product_dict = dict(zip(column_names, fetched_product))
                product = Product()
                product.productify(product_dict)
                products.append(product)

            return products

        except mysql.connector.Error as err:
            print("Error:", err)


# example usage
db = Database()
db.initialise()
products = db.get_products_by_search_input("toy")
