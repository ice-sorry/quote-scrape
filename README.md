# Quote Scraper

A Python-based web scraper that extracts quotes from [Quotes to Scrape](https://quotes.toscrape.com/) website using Selenium WebDriver. The scraper collects quotes by iterating through all authors and their associated tags, then saves the data to a CSV file.

## Project Structure

```
quote-scrape/
├── main.py                 # Main entry point
├── README.md              # This file
├── .env                   # Environment configuration
├── scripts/
│   ├── scraper.py         # Core scraping logic
│   ├── quote.py           # Quote data model
│   └── aws.py             # (Reserved for future AWS integration)
├── notebooks/
│   └── bot.ipynb          # Jupyter notebook version
└── configs/               # Configuration files (currently empty)
```

## Prerequisites

- Python
- Firefox browser
- GeckoDriver (automatically managed by webdriver-manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd quote-scrape
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - pandas
   - selenium
   - webdriver-manager
   - python-dotenv
   - loguru

## Configuration

- `SCRAPE_URL`: The base URL for scraping (default: https://quotes.toscrape.com/search.aspx)
- `EMPTY_QUOTE_TAGS`: Placeholder value for empty tag selections (default: "----------")
- `WEBDRIVER_WAIT_TIME`: Timeout for WebDriver waits in seconds (default: 10)

## Usage

Run the scraper:

```bash
python main.py
```

## Output

The scraper generates `quotes.csv` with the following columns:
- `text`: The quote content
- `author`: The author of the quote
- `tags`: Comma-separated list of tags associated with the quote