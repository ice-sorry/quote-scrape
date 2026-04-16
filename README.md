# Quote Scraper

A Python-based web scraper that extracts quotes from [Quotes to Scrape](https://quotes.toscrape.com/) website using Selenium WebDriver, then saves the data to a CSV file.

## Project Structure

```
quote-scrape/
├── main.py                 # Main entry point
├── README.md              # This file
├── .env                   # Environment configuration
├── scripts/
│   ├── scraper.py         # Core scraping logic
│   ├── quote.py           # Quote data model
│   └── aws.py             # AWS integration
```

## Prerequisites

- Python
- Firefox browser
- GeckoDriver (automatically managed by webdriver-manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ice-sorry/quote-scrape.git
   cd quote-scrape
   ```

2. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with the following environment variables:

### Required Variables

**Scraping Configuration:**
- `SCRAPE_URL`: The base URL for scraping (default: `https://quotes.toscrape.com/`)
- `WEBDRIVER_WAIT_TIME`: Timeout for WebDriver waits in seconds (e.g., `10`)

**AWS S3 Configuration (for uploading results):**
- `ACCESS_KEY`: AWS access key ID for S3 authentication. **Required only in local environment.**
- `ACCESS_SECRET`: AWS secret access key for S3 authentication. **Required only in local environment.**
- `BUCKET_NAME`: Name of the S3 bucket where quotes will be uploaded
- `BUCKET_FILE`: Object key/path for the uploaded file in S3 (e.g., `quotes.csv`)

## Cron

The repo contains the `enable_cron.sh` and `disable_cron.sh` files to serve as a way to toggle the automated running of the script. This is for demonstration purposes only.

The default runtime for the cron is **every Monday at 8:00 UTC**.

## Usage

Run the scraper:

```bash
python main.py
```

## Output

The scraper generates `quotes.csv` with the following columns:
- `text`: The quote content
- `author`: The author of the quote
- `tags`: Pythonic list of tags that describe the quote