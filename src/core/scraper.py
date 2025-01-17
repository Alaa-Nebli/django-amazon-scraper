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

    def scrape_with_brightdata(self, url):
        """Scrape using Bright Data."""
        try:
            print(f"{COLOR_GREEN}Connecting to {url} with Bright Data...{COLOR_RESET}")
            sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

            with Remote(sbr_connection, options=ChromeOptions()) as driver:
                driver.get(url)
                print('Navigated! Scraping page content...')
                html = driver.page_source
                print(f"{COLOR_GREEN}Scraping {url} complete with Bright Data!{COLOR_RESET}")
                return html

        except Exception as e:
            print(f"{COLOR_RED}Bright Data error occurred: {str(e)}{COLOR_RESET}")
            return None

    def scrape_with_scraperapi(self, url):
        """Scrape using ScraperAPI."""
        try:
            print(f"{COLOR_GREEN}Connecting to {url} with ScraperAPI...{COLOR_RESET}")
            proxies = {"https": SCRAPERAPI_PROXY}
            response = requests.get(url, proxies=proxies, verify=False)
            response.raise_for_status()
            print(f"{COLOR_GREEN}Scraping {url} complete with ScraperAPI!{COLOR_RESET}")
            return response.text

        except Exception as e:
            print(f"{COLOR_RED}ScraperAPI error occurred: {str(e)}{COLOR_RESET}")
            return None

    def scrape(self):
        """Main scrape method with fallback logic and retries."""
        print(f"{COLOR_GREEN}Starting scraping process for {self.url}...{COLOR_RESET}")
        
        retry_attempts = 3
        retry_delays = [30, 60, 120]  # 30 seconds, 1 minute, 2 minutes

        for attempt in range(1, retry_attempts + 1):
            print(f"{COLOR_GREEN}Scrape attempt {attempt} of {retry_attempts}{COLOR_RESET}")

            # Try Bright Data first
            html = self.scrape_with_brightdata(self.url)
            if html:
                return html

            # Fallback to ScraperAPI if Bright Data fails
            print(f"{COLOR_RED}Bright Data failed. Trying ScraperAPI...{COLOR_RESET}")
            html = self.scrape_with_scraperapi(self.url)
            if html:
                return html

            # If both fail, wait before retrying
            if attempt < retry_attempts:
                delay = retry_delays[attempt - 1]
                print(f"{COLOR_RED}Both methods failed. Retrying in {delay} seconds...{COLOR_RESET}")
                time.sleep(delay)

        # If all attempts fail
        print(f"{COLOR_RED}All scrape attempts failed. Exiting.{COLOR_RESET}")
        exit(1)
