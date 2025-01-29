from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import os

from product import Product


class WebScraper:
    def __init__(self, search: str) -> None:
        self.search: str = search
        self.url = f"https://www.vinted.co.uk/catalog?search_text={self.input_validate()}"
        self.products = []

    def input_validate(self):
        search = self.search.strip()
        search.replace(" ", "%20")
        return search

    def initialise_driver(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")  # Run in headless mode
        else:
            chrome_options.add_argument("--disable-headless")  # Run in headless mode

        chrome_options.add_argument("--disable-gpu")  # Better performance
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

            if not product_cards:
                print("No products found.")
                return []

            urls = []

            for card in product_cards:
                card_urls = card.find_elements(By.TAG_NAME, "a")

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

            accept_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_button.click()

            time.sleep(2)

        except Exception as e:
            print("Scraped product function failed", e)

    def scrape_product(self, url: str, driver: webdriver.Chrome):
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='item-page-sidebar-content']")))

            product_info = driver.find_element(By.CSS_SELECTOR, "div[class='item-page-sidebar-content']")

            summary = product_info.find_element(By.CSS_SELECTOR, "div[data-testid='item-page-summary-plugin']").text.split("\n")

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

            product_details = {}
            n = len(details)
            while n > 0:
                val, key = details.pop(), details.pop()
                product_details[key] = val

                n = len(details)

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
        urls = self.fetch_urls()
        driver = self.initialise_driver(headless=False)
        counter = 0

        if urls and driver:
            self.accept_cookies(url=urls[0], driver=driver)
            for i, url in enumerate(urls):
                if counter >= limit and limit != 0:
                    break

                print(f"Product {i}/{len(urls) if not limit else limit}")
                product = self.scrape_product(url=url, driver=driver)
                if product:
                    product.display()
                    self.products.append(product)
                    if caching:
                        self.cache(product)
                        print()

                counter += 1

        driver.close()
        return self.products


    def cache(self, product):
        file_name = f"{self.search}-data.json"

        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                json.dump([], file, indent=4)

        with open(file_name, "r+") as file:
            try:
                products = json.load(file)
            except json.JSONDecodeError:
                products = []

            products.append(product.__dict__)

            file.seek(0)
            json.dump(products, file, indent=4)

        print("Cached product: ", product.title)


    def full_cache(self):
        import json

        total_json = [product_object.__dict__ for product_object in self.products]

        with open(f"{self.search}-data.json", "w+") as file:
            json.dump(total_json, file, indent=4)

        print("Successfully cached data to:", f"{self.search}-data.json")

