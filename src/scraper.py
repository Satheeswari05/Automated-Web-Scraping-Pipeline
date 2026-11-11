
import requests
import pandas as pd
import json
import time
import logging

from bs4 import BeautifulSoup
from pathlib import Path

# Website to scrape
BASE_URL = "https://books.toscrape.com/"

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Create output directories if needed
DATA_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# Request settings
HEADERS = {
    "User-Agent": "EducationalBookScraper/1.0"
}

REQUEST_DELAY = 1  # seconds between requests
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def fetch_page(url):
    """Fetch a webpage with retries and basic error handling."""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Fetching: {url}")

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            response.raise_for_status()

            time.sleep(REQUEST_DELAY)

            return response.text

        except requests.RequestException as error:
            logging.warning(
                f"Attempt {attempt} failed: {error}"
            )

            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)

    logging.error(f"Failed to fetch: {url}")
    return None
def parse_books(html):
    """Extract book information from a catalogue page."""

    soup = BeautifulSoup(html, "html.parser")

    books = []

    book_cards = soup.select("article.product_pod")

    for card in book_cards:

        title = card.h3.a["title"]

        price = card.select_one(
            ".price_color"
        ).get_text(strip=True)

        availability = card.select_one(
            ".availability"
        ).get_text(strip=True)

        rating_element = card.select_one(
            "p.star-rating"
        )

        rating = rating_element.get("class")[1]

        link = card.h3.a["href"]

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "product_url": link
        })

    return books

def scrape_all_books():
    """Scrape books from all catalogue pages."""

    all_books = []
    page_number = 1

    while True:
        if page_number == 1:
            page_url = BASE_URL
        else:
            page_url = (
                f"{BASE_URL}catalogue/page-{page_number}.html"
            )

        html = fetch_page(page_url)

        if html is None:
            break

        books = parse_books(html)

        if not books:
            break

        all_books.extend(books)

        logging.info(
            f"Page {page_number}: {len(books)} books collected"
        )

        page_number += 1

    return all_books

def save_data(books):
    """Save scraped books as CSV and JSON."""

    if not books:
        logging.warning("No books available to save.")
        return

    df = pd.DataFrame(books)

    # Save CSV
    csv_path = DATA_DIR / "books.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # Save JSON
    json_path = DATA_DIR / "books.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

    logging.info(f"CSV saved: {csv_path}")
    logging.info(f"JSON saved: {json_path}")

def generate_report(books):
    """Generate summary statistics for scraped books."""

    if not books:
        logging.warning("No data available for report.")
        return

    df = pd.DataFrame(books)

    # Convert prices into numeric values
    df["price_numeric"] = (
    df["price"]
    .str.replace(r"[^\d.]", "", regex=True)
    .astype(float)
)
    total_books = len(df)
    average_price = df["price_numeric"].mean()
    highest_price = df["price_numeric"].max()
    lowest_price = df["price_numeric"].min()

    rating_counts = df["rating"].value_counts()

    report = f"""
BOOK SCRAPING SUMMARY REPORT
============================

Total Books Scraped: {total_books}

Average Price: £{average_price:.2f}
Highest Price: £{highest_price:.2f}
Lowest Price: £{lowest_price:.2f}

Rating Distribution:
{rating_counts.to_string()}
"""

    report_path = REPORT_DIR / "summary_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    logging.info(f"Report saved: {report_path}")

def main():
    """Run the complete scraping pipeline."""

    logging.info("Starting Book Scraping Pipeline...")

    books = scrape_all_books()

    if books:
        save_data(books)
        generate_report(books)

        logging.info(
            f"Scraping completed! Total books: {len(books)}"
        )
    else:
        logging.warning("Scraping finished without collecting data.")


if __name__ == "__main__":
    main()
