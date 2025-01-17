import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from decouple import config
import requests

# Load color codes from .env file
COLOR_RED = config("COLOR_RED")
COLOR_GREEN = config("COLOR_GREEN")
COLOR_RESET = config("COLOR_RESET")

# Bright Data Auth key from .env
AUTH = config("SBR_AUTH", default="")
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

# ScraperAPI key from .env
SCRAPERAPI_AUTH = config("SCRAPERAPI_AUTH", default="")
SCRAPERAPI_PROXY = "scraperapi.retry_404=true:81e3790ed62fe2c530e84392506a61fe@proxy-server.scraperapi.com:8001"


class Scraper:
    def __init__(self, url):
        self.url = url
        self.sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        self.driver = None

    # Still not Tested 
    # def navigate_and_scrape_amazon(self):
    #     """Navigate Amazon pages and scrape content."""
    #     attempts = 0
    #     max_pages = 5  # Limit to avoid infinite loops
    #     scraped_data = []

    #     try:
    #         with Remote(self.sbr_connection, options=ChromeOptions()) as driver:
    #             driver.get(self.url)
    #             wait = WebDriverWait(driver, 10)
    #             print(f"{COLOR_GREEN}Navigated to {self.url}{COLOR_RESET}")

    #             for page in range(1, max_pages + 1):
    #                 print(f"{COLOR_GREEN}Scraping page {page}...{COLOR_RESET}")
                    
    #                 # Wait for product container to load
    #                 wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))
                    
    #                 # Extract product details
    #                 products = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")
    #                 for product in products:
    #                     try:
    #                         title = product.find_element(By.CSS_SELECTOR, "h2 a span").text
    #                         link = product.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
    #                         price = product.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").text
    #                         scraped_data.append({"title": title, "link": link, "price": price})
    #                     except Exception as e:
    #                         print(f"{COLOR_RED}Error extracting product: {str(e)}{COLOR_RESET}")
                    
    #                 # Check for "Next" button and navigate
    #                 try:
    #                     next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.a-last a")))
    #                     ActionChains(driver).move_to_element(next_button).click().perform()
    #                     time.sleep(2)  # Small delay to mimic human behavior
    #                 except Exception:
    #                     print(f"{COLOR_RED}No more pages or navigation error on page {page}.{COLOR_RESET}")
    #                     break

    #             print(f"{COLOR_GREEN}Scraping complete!{COLOR_RESET}")
    #             return scraped_data

    #     except Exception as e:
    #         print(f"{COLOR_RED}Error navigating Amazon: {str(e)}{COLOR_RESET}")
    #         return scraped_data
        

    def scrape_with_brightdata(self, url):
        """Scrape using Bright Data."""
        attempts = 0
        wait_times = [30, 60, 300]  # 30 seconds, 1 minute, 5 minutes

        while attempts < len(wait_times):
            try:
                print(f"{COLOR_GREEN}Attempt {attempts + 1}: Connecting to {url} with Bright Data...{COLOR_RESET}")
                sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

                with Remote(sbr_connection, options=ChromeOptions()) as driver:
                    driver.get(url)
                    print('Navigated! Scraping page content...')
                    html = driver.page_source
                    print(f"{COLOR_GREEN}Scraping {url} complete with Bright Data!{COLOR_RESET}")
                    return html

            except Exception as e:
                print(f"{COLOR_RED}Bright Data error occurred: {str(e)}{COLOR_RESET}")
                attempts += 1
                if attempts < len(wait_times):
                    wait_time = wait_times[attempts - 1]
                    print(f"{COLOR_RED}Retrying in {wait_time} seconds...{COLOR_RESET}")
                    time.sleep(wait_time)
                else:
                    print(f"{COLOR_RED}Bright Data failed after {attempts} attempts.{COLOR_RESET}")
                    return None

    def scrape_with_scraperapi(self, url):
        """Scrape using ScraperAPI."""
        attempts = 0
        wait_times = [30, 60, 300]  # 30 seconds, 1 minute, 5 minutes
        proxies = {"https": SCRAPERAPI_PROXY}

        while attempts < len(wait_times):
            try:
                print(f"{COLOR_GREEN}Attempt {attempts + 1}: Connecting to {url} with ScraperAPI...{COLOR_RESET}")
                response = requests.get(url, proxies=proxies, verify=False)
                
                response.raise_for_status()
                print(f"{COLOR_GREEN}Scraping {url} complete with ScraperAPI!{COLOR_RESET}")
                return response.text

            except Exception as e:
                print(f"{COLOR_RED}ScraperAPI error occurred: {str(e)}{COLOR_RESET}")
                attempts += 1
                if attempts < len(wait_times):
                    wait_time = wait_times[attempts - 1]
                    print(f"{COLOR_RED}Retrying in {wait_time} seconds...{COLOR_RESET}")
                    time.sleep(wait_time)
                else:
                    print(f"{COLOR_RED}ScraperAPI failed after {attempts} attempts.{COLOR_RESET}")
                    return None

    def scrape(self):
        """Main scrape method with fallback logic."""
        print(f"{COLOR_GREEN}Starting scraping process for {self.url}...{COLOR_RESET}")
        
        # Try Bright Data first
        html = self.scrape_with_brightdata(self.url)
        if html:
            return html

        # Fallback to ScraperAPI if Bright Data fails
        print(f"{COLOR_RED}Falling back to ScraperAPI...{COLOR_RESET}")
        html = self.scrape_with_scraperapi(self.url)
        if html:
            return html

        # If both fail
        print(f"{COLOR_RED}Both Bright Data and ScraperAPI failed. Exiting.{COLOR_RESET}")
        exit(1)
