from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from decouple import config

AUTH = config("SBR_AUTH", default="")

SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape(url : str):
    print('Connecting to Scraping {url}...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(url)
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
if __name__ == '__main__':
  url = 'https://www.amazon.com/s?k=home'
  scrape(url)