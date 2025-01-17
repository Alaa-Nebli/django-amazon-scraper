import requests
from bs4 import BeautifulSoup
from decouple import config
from scraper import Scraper
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, parse_qs

# Load color codes from .env file
COLOR_RED = config("COLOR_RED")
COLOR_GREEN = config("COLOR_GREEN")
COLOR_RESET = config("COLOR_RESET")


class AmazonScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.products_data = []

    def extract_products_list(self, html):
        """Extract product list from search results page."""
        soup = BeautifulSoup(html, "html.parser")
        products_list = soup.find_all("div", class_="s-result-item")
        product_links = []

        for product in products_list:
            try:
                product_link = product.find("a", class_="a-link-normal").get("href")
                full_product_link = urljoin("https://www.amazon.com", product_link)
                product_links.append(full_product_link)
            except Exception as e:
                print(f"{COLOR_RED}Error extracting product link: {e}{COLOR_RESET}")

        return product_links

    def extract_product_details(self, url):
        """Extract all required details from a product page."""
        try:
            print(f"{COLOR_GREEN}Scraping product page: {url}{COLOR_RESET}")
            html = Scraper(url).scrape()
            soup = BeautifulSoup(html, "html.parser")

            # Extract details
            asin = self.get_asin_from_url(url)
            title = soup.find("span", id="productTitle")
            title = title.text.strip() if title else "N/A"

            brand = soup.find("a", id="bylineInfo")
            brand = brand.text.strip() if brand else "N/A"

            price = soup.find("span", id="priceblock_ourprice")
            price = price.text.strip() if price else "N/A"

            rating = soup.find("span", class_="a-icon-alt")
            rating = rating.text.strip() if rating else "N/A"

            review_count = soup.find("span", id="acrCustomerReviewText")
            review_count = review_count.text.strip() if review_count else "N/A"

            primary_image = soup.find("img", id="landingImage")
            primary_image_url = primary_image.get("src") if primary_image else "N/A"

            secondary_images = soup.find_all("img", class_="a-dynamic-image")
            secondary_image_urls = [img.get("src") for img in secondary_images if img.get("src")]

            description = soup.find("div", id="productDescription")
            description_text = description.text.strip() if description else "N/A"

            specs_table = soup.find("table", id="productDetails_techSpec_section_1")
            specs = specs_table.text.strip() if specs_table else "N/A"

            normal_delivery = soup.find("div", id="ddmDeliveryMessage")
            normal_delivery = normal_delivery.text.strip() if normal_delivery else "N/A"

            fastest_delivery = soup.find("span", class_="a-text-bold")
            fastest_delivery = fastest_delivery.text.strip() if fastest_delivery else "N/A"

            return {
                "ASIN": asin,
                "Title": title,
                "Url": url,
                "Brand": brand,
                "Price": price,
                "Rating": rating,
                "Review_count": review_count,
                "Primary_image_url": primary_image_url,
                "Secondary_image_url": secondary_image_urls,
                "Description": description_text,
                "Specs": specs,
                "Normal_Delivery_date": normal_delivery,
                "Fastest_Delivery_date": fastest_delivery,
            }
        except Exception as e:
            print(f"{COLOR_RED}Error scraping product page: {e}{COLOR_RESET}")
            return {}

    @staticmethod
    def get_asin_from_url(url):
        """Extract ASIN from the product URL."""
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("/")
        for part in path_parts:
            if len(part) == 10 and part.isalnum():
                return part
        return "N/A"

    def scrape_products(self):
        """Main function to scrape search results and individual product pages."""
        print(f"{COLOR_GREEN}Starting scraping for {self.base_url}{COLOR_RESET}")
        html = Scraper(self.base_url).scrape()
        product_links = self.extract_products_list(html)

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.extract_product_details, url): url for url in product_links}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    details = future.result()
                    if details:
                        self.products_data.append(details)
                except Exception as e:
                    print(f"{COLOR_RED}Error processing future for URL {url}: {e}{COLOR_RESET}")

        print(f"{COLOR_GREEN}Scraping completed!{COLOR_RESET}")
        return self.products_data


if __name__ == "__main__":
    url = "https://www.amazon.com/s?k=home"
    scraper = AmazonScraper(url)
    data = scraper.scrape_products()

    for product in data:
        print(product)
