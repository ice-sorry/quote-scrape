import pandas as pd
import numpy as np
import os
import re
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
    # options.set_preference("dom.webdriver.enabled", False)
    # options.set_preference('useAutomationExtension', False)

    logger.info('Initializing GeckoDriver...')

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, WEBDRIVER_WAIT_TIME)
    
    logger.info('GeckoDriver initialized successfully.')

    return driver, wait

def get_authors(wait: WebDriverWait) -> list[str]:
    authors = wait.until(EC.element_to_be_clickable((By.ID, "author"))).find_elements(By.TAG_NAME, "option")
    authors = [a.get_attribute("value") for a in authors if a.get_attribute("value") != EMPTY_QUOTE_TAGS]
    return authors

def get_tags(driver: webdriver) -> list[Quote]:
    tags = driver.find_element(By.ID, "tag").find_elements(By.TAG_NAME, "option")
    return [t.get_attribute("value") for t in tags if t.get_attribute("value") != EMPTY_QUOTE_TAGS]

def merge_quotes(quote_list: list[Quote]):
    """Given a list of Quote objects, merge quotes with the same text and author by combining their tags into a single quote with all unique tags.

    Args:
        quote_list (list[Quote]): A list of Quote objects to be merged. May contain multiple Quote objects with the same text and author but different tags.

    Returns:
        list[Quote]: A list of Quote objects with unique text and author values.
    """
    
    merged = {}
    for quote in quote_list:
        key = (quote.text, quote.author)
        if key not in merged:
            merged[key] = set(quote.tags)
        else:
            merged[key].update(quote.tags)
    
    return [Quote.__from_dict__({
        "text": text,
        "author": author,
        "tags": list(tags)
    }) for (text, author), tags in merged.items()]

def scrape_all_quotes() -> list[Quote]:
    """Scrape all quotes for each author and their associated tags from the website.

    Args:

        authors (list): A list of author names to scrape quotes for.

    Returns:
        list[Quote]: A list of scraped Quote objects.
    """    
    quote_list = []
    
    driver, wait = init_bot()
    driver.get(SCRAPE_URL)
    # authors = get_authors(wait)
    authors = ['Albert Einstein']
    
    for author in authors:
        author_select = wait.until(EC.element_to_be_clickable((By.ID, "author")))
        author_select.click()
        option = author_select.find_element(By.XPATH, f""".//option[@value="{author}"]""")
        option.click()
        
        tags = get_tags(driver)
        
        for tag in tags:
            tag_select = wait.until(EC.element_to_be_clickable((By.ID, "tag")))
            tag_select.click()
            option = tag_select.find_element(By.XPATH, f".//option[@value='{tag}']")
            option.click()
            
            search = wait.until(EC.element_to_be_clickable((By.NAME, "submit_button")))
            search.click()
            
            # Wait for page refresh, which will likely contain new quote data
            wait.until(EC.staleness_of(search))
            
            try:
                quotes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))
                logger.info(f"[{author}] Scraped {len(quotes)} quotes for tag '{tag}'")
                quote_list.extend([Quote.__from_element__(q) for q in quotes])
            except TimeoutException:
                logger.error(f"Timeout while waiting for quotes to load for author '{author}' and tag '{tag}'. Skipping this combination.")
                pass

    # For cases where a quote contains multiple tags, combine them together into a single quote with all tags
    merged_quotes = merge_quotes(quote_list=quote_list)
    return merged_quotes