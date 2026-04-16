import pandas as pd
from loguru import logger
from pathlib import Path
from scripts.scraper import scrape_all_quotes

OUTPUT_PATH = Path(__file__).resolve().parent / 'output' / 'quotes.csv'

def main():
    logger.info("Starting quote scraping process...")
    
    try:
        quotes = scrape_all_quotes()
    except Exception as e:
        logger.error(f"An error occurred while scraping quotes: {e}")
        return

    try:
        df = pd.DataFrame([q.__dict__ for q in quotes])
        df.to_csv(OUTPUT_PATH, index=False)
        
        logger.info(f"Scraped {len(quotes)} unique quotes and saved to '{OUTPUT_PATH}'.")
    except Exception as e:
        logger.error(f"An error occurred in file writing: {e}")


if __name__ == "__main__":
    main()