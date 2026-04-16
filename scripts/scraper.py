import os
import time
import random
from dotenv import load_dotenv
from pathlib import Path
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from scripts.quote import Quote

BASE_PATH = Path(__file__).resolve().parent.parent
load_dotenv(BASE_PATH / '.env')

def __require_env(key):
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable '{key}' is required but not set.")
    return value

EMPTY_QUOTE_TAGS =  __require_env("EMPTY_QUOTE_TAGS")
SCRAPE_URL = __require_env("SCRAPE_URL")
WEBDRIVER_WAIT_TIME = int(__require_env("WEBDRIVER_WAIT_TIME"))

def init_bot():
    """Generates and initializes a GeckoDriver instance with appropriate options for web scraping.
    """
    options = Options()
    
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-web-security")
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)

    logger.info('Initializing GeckoDriver...')

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, WEBDRIVER_WAIT_TIME)
    
    logger.info('GeckoDriver initialized successfully.')

    return driver, wait
    
def check_next_page(wait):
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.next > a")))
        return next_button.get_attribute("href")
    except Exception as e:
        logger.error(f'Error during next page check: {e}')
        
    return None

def scrape_all_quotes(retries=5, base_delay=1) -> list[Quote]:
    """Scrapes all quotes from the website specified in the environment variable 'SCRAPE_URL' using Selenium WebDriver. The function navigates through all pages of quotes, extracts the quote text, author, and tags, and returns a list of Quote objects

    Returns:
        list[Quote]: A list of scraped Quote objects.
    """
    
    driver, wait = init_bot()
    
    quote_list = []
    
    BASE_URL = __require_env("SCRAPE_URL")
    current_url = BASE_URL
    
    while current_url is not None:            
        try:
            current_retries = 0
            
            driver.get(current_url)
            quotes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))
            logger.info(f"Scraped {len(quotes)} quotes from {current_url}")
            quote_list.extend([Quote.__from_element__(q) for q in quotes])
            
            current_url = check_next_page(wait)
        except TimeoutException as e:
            logger.error(f"Timeout while loading page: {current_url} - {e}")
            
            if current_retries < retries:
                current_retries += 1
                delay = (base_delay * 2 ** current_retries) + random.uniform(0, 1) # Exponential backoff with jitter
                logger.error(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error("Max retries exceeded.")
                break

    driver.quit()
    
    return quote_list
