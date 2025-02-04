from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tempfile
import time
import json
import os

from product import Product


class WebScraper:
    def __init__(self, search: str) -> None:
        self.search: str = search
        self.url = f"https://www.vinted.co.uk/catalog?search_text={self.input_validate()}"
        self.products = []

    def input_validate(self) -> str:
        # remove trailing spaces 
        search = self.search.strip()
        # replace spaces with %20 to make the search input suitable for the url 
        search.replace(" ", "%20")
        return search

    def initialise_driver(self):

        # These settings are specfic for the scraper to run on a github codespace. 

        # Modify chrome options for the chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Better performance

        # Use a temporary directory for the user data
        user_data_dir = tempfile.mkdtemp() 
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        return webdriver.Chrome(options=chrome_options)


    def fetch_urls(self):
        try:
            # Initialize the driver
            driver = self.initialise_driver()
            driver.get(self.url)

            # Wait for the product grid to load
            wait = WebDriverWait(driver, 5)
            product_cards = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[class='feed-grid__item']")
                )
            )

            # if no product cards are found return and empty array
            if not product_cards:
                print("No products found.")
                return []

            urls = []

            # loop through each product on the page 
            for card in product_cards:
                card_urls = card.find_elements(By.TAG_NAME, "a")

                # save the product url to go back to later 
                url = card_urls[1].get_attribute('href')
                urls.append(url)

                print("card url", url)

            driver.quit()

            return urls

        except Exception as e:
            print(f"An error occurred: {e}")


    def accept_cookies(self, url: str, driver: webdriver.Chrome):
        print("Accepting cookies")
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 5)

            # wait until cookies appear
            accept_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            # click "Accept Cookies" button
            accept_button.click()

            # give time to allow the rest of the page to load
            time.sleep(2)

        except Exception as e:
            print("Scraped product function failed", e)

    def scrape_product(self, url: str, driver: webdriver.Chrome):
        try:
            # go to product by url 
            driver.get(url)
            # wait for page content to load
            wait = WebDriverWait(driver, 10)

            # wait until the product data has loaded
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='item-page-sidebar-content']")))

            # find the main information div
            product_info = driver.find_element(By.CSS_SELECTOR, "div[class='item-page-sidebar-content']")

            # find the other main information div
            summary = product_info.find_element(By.CSS_SELECTOR, "div[data-testid='item-page-summary-plugin']").text.split("\n")

            # create new instance of product
            product = Product()

            title = summary[0]
            product.title = title

            size_quality = summary[1].split("·")

            size = size_quality[0]
            product.size = size

            quality = size_quality[1]
            product.quality = quality

            pricing = product_info.find_element(By.CSS_SELECTOR, "div[data-testid='item-sidebar-price-container']").text.split("\n")
            product.price = float(pricing[0][1:])
            product.buyer_protection_price = float(pricing[1][1:])

            description = product_info.find_element(By.CSS_SELECTOR, "div[itemprop='description']").text
            product.description = description

            details_list = product_info.find_element(By.CSS_SELECTOR, "div[class='details-list details-list--details']")
            details = details_list.find_elements(By.CSS_SELECTOR, "div[class='details-list__item-value']")
            details = [detail.text for detail in details]

            postage = product_info.find_element(By.CSS_SELECTOR, "div[data-testid='item-shipping-banner']").text
            postage = float(postage.split("£")[-1])
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

            return product


        except Exception as e:
            print("Scraped product function failed", e)
            return None

    def scrape(self, limit=5, caching=True):
        # get all product urls 
        urls = self.fetch_urls()

        # create new chrome driver
        driver = self.initialise_driver()
        
        # this counter will be used as a limiter 
        counter = 0

        # if urls were found and the driver was created correctly 
        if urls and driver:
            # accept cookies on the first url but dont scrape, this is just to have cookies accepted
            # on all future product pages so the unexpected html doesnt get in the way
            self.accept_cookies(url=urls[0], driver=driver)

            # loop through for index of url and actual url 
            for i, url in enumerate(urls):
                # if the limit has been reached end scraping
                if counter >= limit and limit != 0:
                    break

                print(f"Product {i}/{len(urls) if not limit else limit}")
                # scrape product information 
                product = self.scrape_product(url=url, driver=driver)

                # if information is found 
                if product:
                    product.display()
                    self.products.append(product)
                    if caching:
                        # save the data to a json file
                        self.cache(product)
                        print()

                counter += 1

        driver.close()
        return self.products


    def cache(self, product):
        # create file name for the data 
        file_name = f"{self.search}-data.json"

        # if the file doesnt already exist, make one
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                json.dump([], file, indent=4)

        # open the json file
        with open(file_name, "r+") as file:
            # if there are products in the file read them and store them
            # in an array, if there are no products use an empty array
            try:
                products = json.load(file)
            except json.JSONDecodeError:
                products = []

            # add the product in a hashmap format 
            products.append(product.__dict__)

            file.seek(0)
            # write the product data in a json format 
            json.dump(products, file, indent=4)

        print("Cached product: ", product.title)


    def full_cache(self):
        import json

        total_json = [product_object.__dict__ for product_object in self.products]

        with open(f"{self.search}-data.json", "w+") as file:
            json.dump(total_json, file, indent=4)

        print("Successfully cached data to:", f"{self.search}-data.json")

