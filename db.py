# Import the mysql connector module to access the sql database
import mysql.connector
# Import my Product object
from product import Product

# This is the database object to handle access to the sql database. This object reduces code duplication by using the Database object to get and add products to the database. It also simplifies the process in the scraping and main files as instead of writing the sql access with the database config rewritten, Database().insert_product(product) can be used instead
class Database:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "jamie",
            "password": "password",
            "database": "products_database"
        }

        self.connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.connection.cursor()

    # check if the inputted product is already in the database
    def is_a_duplicate(self, product: Product) -> bool:
        # This is the search input of the product the user is looking for
        search_input: str = product.search_input

        # sql query to get all products with inputted search input
        sql: str = "SELECT * FROM products WHERE search_input=%s"

        # execute the command
        self.cursor.execute(sql, (search_input,))
        # this is all of the product information in the database matching the search input
        fetched_products= self.cursor.fetchall()

        # this is the column which url is stored in the database
        url_column_index = 14

        # loop through each product and compare the urls, this is becuase the urls should be unique
        if fetched_products:
            for fetched_product in fetched_products:
                if fetched_product[url_column_index] == product.url:
                    return True

        return False

    # add products to database
    def insert_products_to_db(self, products: list[Product]) -> None:
        # add each product to the database individually
        for product in products:
            # add the product to the database
            self.insert_product(product)

        self.connection.commit()


    def insert_product(self, product: Product) -> None:
        # check if the product is already in the database
        if self.is_a_duplicate(product):
            print("Product is a duplicate")
            return

        # sql query to add the product and its data into the database
        sql: str = """
        INSERT INTO products
        (title, price, buyer_protection_price, postage, brand, colour, size, quality, `condition`, location, payment_options, views, description, url, uploaded, search_input)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # values to be used in the sql command
        values: tuple = (
            product.title,
            product.price,
            product.buyer_protection_price,
            product.postage,
            product.brand,
            product.colour,
            product.size,
            product.quality,
            product.condition,
            product.location,
            product.payment_options,
            product.views,
            product.description,
            product.url,
            product.uploaded,
            product.search_input
        )

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            print("Error:", err)

    def get_products_by_search_input(self, search_input: str) -> list[Product]:
        # sql query to get all of the products which match the inputted search input
        sql: str = "SELECT * FROM products WHERE search_input=%s"

        try:
            self.cursor.execute(sql, (search_input,))
            # this is all of the product information of the matching search input in the database stored in an array
            fetched_products = self.cursor.fetchall()

            sql_description = self.cursor.description
            column_names: list[str | any] = [desc[0] for desc in sql_description]
            # empty array to store the each Product object
            products = []

            # turn all of the products recieved into Product objects
            if fetched_products:
                for fetched_product in fetched_products:
                    # turn the information into a dictionary using the sql database column names and the product data
                    product_dict: dict = dict(zip(column_names, fetched_product))
                    # instantiate new instance of Product
                    product = Product()
                    # store the product dictionary information into the product object
                    product.productify(product_dict)
                    # add the Product object to the array of objects
                    products.append(product)

            return products

        except mysql.connector.Error as err:
            print("Error:", err)
            return []

