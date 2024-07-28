from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import List
import time

class Scraper:
    def __init__(self, base_url: str, proxy: str = None):
        self.base_url = base_url
        self.proxy = proxy
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run headless Chrome
        chrome_options.add_argument('--disable-gpu')
        if self.proxy:
            chrome_options.add_argument(f'--proxy-server={self.proxy}')
        
        # Path to chromedriver executable in the app directory
        self.driver_service = Service('./app/chromedriver')
        self.driver = webdriver.Chrome(service=self.driver_service, options=chrome_options)

    def fetch_page(self, url: str, retries: int = 3, delay: int = 5):
        for _ in range(retries):
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".products")))
                page_content = self.driver.page_source
                return page_content
            except Exception as e:
                print(f"Error fetching {url}: {e}, retrying in {delay} seconds...")
                time.sleep(delay)
        return None

    def scrape_page(self, page_number: int) -> List[dict]:
        url = self.base_url
        if page_number == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}page/{page_number}/"
        page_content = self.fetch_page(url)
        
        if not page_content:
            print(f"Failed to fetch page content from {url}")
            return []


        soup = BeautifulSoup(page_content, 'html.parser')
        products = []

        for product in soup.select(".product"):
            link_element = product.select_one('.woo-loop-product__title a')
            href_link = link_element['href']

            split_link = href_link.split('/')

            title = split_link[-2]
            price_element = product.select_one(".woocommerce-Price-amount")
            image_element = product.select_one("img")

            # title = title_element.get_text(strip=True) if title_element else "N/A"
            price = price_element.get_text(strip=True)[1:] if price_element else "N/A"
            image_url = image_element["src"] if image_element else "N/A"

            products.append({
                "product_title": title,
                "product_price": price,
                "image_url": image_url
            })
        return products

    def scrape(self, pages: int) -> List[dict]:
        all_products = []
        for page_number in range(1, pages + 1):
            products = self.scrape_page(page_number)
            if products:
                all_products.extend(products)
            else:
                break
        self.driver.quit()
        return all_products


def test_scraper():
    scraper = Scraper(base_url="https://dentalstall.com/shop/")
    products = scraper.scrape(pages=1)
    for product in products:
        print(product)

if __name__ == "__main__":
    test_scraper()
