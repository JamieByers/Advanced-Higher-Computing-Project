from re import split
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tempfile
import time
import json
import os
from db import Database

from product import Product


class WebScraper:
    def __init__(self, search_input: str, limit=-1) -> None:
        self.search_input: str = search_input
        self.url: str = f"https://www.vinted.co.uk/catalog?search_text={self.input_validate()}"
        self.products = []
        self.limit: int = limit
        self.database = Database()

    def input_validate(self) -> str:
        # remove trailing spaces
        search = self.search_input.strip()
        # replace spaces with %20 to make the search input suitable for the url
        search.replace(" ", "%20")
        return search

    def initialise_driver(self) -> webdriver.Chrome:

        # These settings are specfic for the scraper to run on a github codespace.

        # Modify chrome options for the chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Better performance

        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--v=1')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Use a temporary directory for the user data
        user_data_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        return webdriver.Chrome(options=chrome_options)

    def fetch_urls(self) -> list[str]:
        # print("Fetching urls")

        # Initialize the driver
        driver = self.initialise_driver()
        driver.get(self.url)
        # Wait for the product grid to load and get each grid item
        wait = WebDriverWait(driver, 10)

        # wait until cookies appear
        accept_button = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )

        time.sleep(1)

        # click "Accept Cookies" button
        accept_button.click()

        # print("Accepted cookies")

        time.sleep(1)
        product_cards = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[class='feed-grid__item']")
            )
        )


        urls = []

        if product_cards:
            for card in product_cards:
                feed_grid_item_content = card.find_element(By.CLASS_NAME, "feed-grid__item-content")
                new_item_box__container = feed_grid_item_content.find_element(By.CLASS_NAME, "new-item-box__container")
                new_item_box__image_container = new_item_box__container.find_element(
                    By.CSS_SELECTOR, ".u-position-relative.u-min-height-none.u-flex-auto.new-item-box__image-container"
                )
                link = new_item_box__image_container.find_element(By.TAG_NAME, "a")
                url: str = link.get_attribute("href")
                urls.append(url)

                # print(url)

        # print("Ended fetch urls")
        return urls

    def accept_cookies(self, url: str, driver: webdriver.Chrome) -> bool:
        # print("Accepting cookies")
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            # wait until cookies appear
            accept_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )

            # give time for the button to load
            time.sleep(2)

            # click "Accept Cookies" button
            accept_button.click()

            time.sleep(1)

            # print("Accepted cookies")

            return True

        except Exception as e:
            print("Accept Cookies Failed (line 105): ", e)
            return False

    def scrape_product(self, url: str, driver: webdriver.Chrome) -> Product:
        # go to product by url
        driver.get(url)
        # wait for page content to load
        wait = WebDriverWait(driver, 10)

        # wait until the product data has loaded
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='item-page-sidebar-content']")))
        time.sleep(1)

        # find the main information div
        product_info = driver.find_element(By.CSS_SELECTOR, "div[class='item-page-sidebar-content']")

        # find the other main information div
        summary = product_info.find_element(By.CSS_SELECTOR, "div[data-testid='item-page-summary-plugin']").text.split("\n")

        # create new instance of product
        product = Product()

        title: str = summary[0]
        product.title = title

        size_quality: str = summary[1].split("·")

        size: str = size_quality[0]
        product.size = size

        
        if len(size_quality) > 1:
            quality: str = size_quality[1]
            product.quality = quality
        else:
            product.quality = ""

        pricing: list[str] = product_info.find_element(By.CSS_SELECTOR, "div[data-testid='item-sidebar-price-container']").text.split("\n")
        product.price = float(pricing[0][1:])
        product.buyer_protection_price = float(pricing[1][1:])

        description: str = product_info.find_element(By.CSS_SELECTOR, "div[itemprop='description']").text
        product.description = description

        details_list = product_info.find_element(By.CSS_SELECTOR, "div[class='details-list details-list--details']")
        details = details_list.find_elements(By.CSS_SELECTOR, "div[class='details-list__item-value']")
        details: list[str] = [detail.text for detail in details]

        postage: str = product_info.find_element(By.CSS_SELECTOR, "div[data-testid='item-shipping-banner']").text
        postage: float = float(postage.split("£")[-1])
        product.postage = postage

        # collect available details on the page and store them in a hashmap
        product_details = {}
        n = len(details)
        while n > 0:
            val, key = details.pop(), details.pop()
            product_details[key] = val

            n = len(details)

        # store the data from the hashmap into the Product instance and if there is no data give a default value
        product.uploaded = product_details.get("Uploaded", "")
        product.condition = product_details.get("Condition", "")
        product.brand = product_details.get("Brand", "")
        product.location = product_details.get("Location", "")
        product.payment_options = product_details.get("Payment options", "")
        product.colour = product_details.get("Colour", "")
        product.views = product_details.get("Views", 0.0)
        product.url = url
        product.search_input = self.search_input

        return product

    def scrape(self, caching=True) -> list[Product]:
        # get all product urls
        urls: list[str] = self.fetch_urls()

        # create new chrome driver
        driver = self.initialise_driver()

        self.database.initialise()

        # this counter will be used as a limiter
        counter: int = 0

        # if urls were found and the driver was created correctly
        if urls and driver:
            # accept cookies on the first url but dont scrape, this is just to have cookies accepted
            # on all future product pages so the unexpected html doesnt get in the way
            self.accept_cookies(url=urls[0], driver=driver)

            # loop through for index of url and actual url
            for i, url in enumerate(urls):
                # if the limit has been reached end scraping
                if counter >= self.limit and self.limit > 0:
                    break

                # print(f"Product {i}/{len(urls) if self.limit <= 0 else self.limit}")
                self.individual_scrape(url, driver, caching)

                counter += 1


        driver.quit()
        return self.products

    def cache(self, product) -> None:
        # create file name for the data
        file_name: str = f"product-data/{self.search_input}-data.json"

        # if the file doesnt already exist, make one
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                json.dump([], file, indent=4)

        # open the json file
        with open(file_name, "r+") as file:
            # if there are products in the file read them and store them
            # in an array, if there are no products use an empty array
            try:
                products: dict = json.load(file)
            except json.JSONDecodeError:
                products = []

            # add the product in a hashmap format
            pd: dict = product.__dict__
            product_url: str = pd["url"]
            product_urls: list[str] = [p["url"] for p in products]

            if product_url not in product_urls:
                products.append(pd)

            file.seek(0)
            # write the product data in a json format to the json file
            json_products: str = json.dumps(products, indent=4)
            file.write(json_products)

    def individual_scrape(self, url, driver, caching) -> Product:
        # scrape the product information of the associated url 
        product: Product = self.scrape_product(url=url, driver=driver)

        # if information is found
        if product:
            # product.display()
            self.products.append(product)
            if caching:
                # save the data to a json file to be used for testing
                self.cache(product)

        # add the scraped product into the database
        self.database.insert_product(product.__dict__)

        return product # return the product data in a product object

    # --------------------------------- OPTIONAL -------------------------------------------

    def decided_scrape(self, threading=False, caching=True):
        if threading:
            return self.thread_scrape(caching)
        else:
            return self.scrape(caching)

    def split_array(self, arr, n):
        base_size = len(arr) // n  # Minimum size of each subarray
        sizes = [base_size] * n    # Start with equal-sized subarrays
        sizes[-1] += len(arr) % n  # Add the remainder to the last subarray

        result = []
        index = 0
        for size in sizes:
            result.append(arr[index:index + size])
            index += size
        return result

    def thread_scrape(self, caching=True):
        urls = self.fetch_urls()
        urls = urls[:min(self.limit, len(urls))]

        self.database.initialise()
        
        max_threads = 5

        split_urls = self.split_array(urls, max_threads)

        threads = []
        for thread_index in range(max_threads):
            driver = self.initialise_driver()
            thread = threading.Thread(target=self.thread_helper, args=(split_urls[thread_index], driver, caching))
            threads.append(thread)
            thread.start()
            thread.join()

        return self.products

    def thread_helper(self, urls, driver, caching):
        products = []
        for url in urls:
            product = self.individual_scrape(url, driver, caching)
            products.append(product)

        return products
    
    def full_cache(self):
        import json

        total_json = [product_object.__dict__ for product_object in self.products]

        with open(f"{self.search_input}-data.json", "w+") as file:
            json.dump(total_json, file, indent=4)

        print("Successfully cached data to:", f"{self.search_input}-data.json")