from selenium import webdriver
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

from product import Product


class WebScraper:
    def __init__(self, search: str) -> None:
        self.search: str = search
        self.url = f"https://www.vinted.co.uk/catalog?search_text={search}"

    def initialise_driver(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")  # Run in headless mode
        else:
            chrome_options.add_argument("--disable-headless")  # Run in headless mode

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

            return urls



        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()

    def scrape_first_product(self, url: str, driver: webdriver.Chrome):
        print("Product scraping at url: ", url)
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            accept_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_button.click()

            time.sleep(2)
            product_info = driver.find_element(By.CSS_SELECTOR, "div[class='item-page-sidebar-content']")
            print("product info", product_info)


        except Exception as e:
            print("Scraped product function failed", e)

    def scrape_product(self, url: str, driver: webdriver.Chrome):
        print("Product scraping at url: ", url)
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

            # NOT WORKING
            # postage = details_list.find_element(By.CSS_SELECTOR, "div[data-testid='item-shipping-banner-price']").text
            # print(postage)

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



            print(product_details)
            # print("title: ", title)
            # print("size: ", size)
            # print("quality: ", quality)
            # print("pricing: ", pricing)
            # print("details list", details_list)
            print()

        except Exception as e:
            print("Scraped product function failed", e)

    def scrape(self):
        urls = self.fetch_urls()
        driver = self.initialise_driver()

        if urls and driver:
            first_url = urls.pop(0)
            self.scrape_first_product(url=first_url, driver=driver)
            for url in urls:
                self.scrape_product(url=url, driver=driver)

        driver.close()

