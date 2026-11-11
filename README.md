# Automated Web Scraping & Data Extraction Pipeline

## Project Overview
This project implements an automated web scraping pipeline using Python to extract structured book information from [Books to Scrape](https://books.toscrape.com/), a website designed for scraping practice.

The extracted information is transformed and exported into CSV and JSON formats. The project also generates an automated summary statistics report.

## Technologies Used
- Python
- Requests
- BeautifulSoup
- Pandas
- JSON

## Features
- Automated webpage extraction
- Custom HTTP request headers
- Request retry mechanism
- Rate limiting
- HTML parsing using BeautifulSoup
- Multi-page scraping (pagination)
- CSV and JSON data exports
- Automated summary statistics report
- Logging and error handling

## Data Extracted
- Book Title
- Price
- Rating
- Availability
- Product URL

## Project Structure
```text
Project_4_Web_Scraping/
│
├── src/
│   └── scraper.py
│
├── data/
│   ├── books.csv
│   └── books.json
│
├── reports/
│   └── summary_report.txt
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python src/scraper.py
```

## Output
The pipeline generates:

- `books.csv` – Structured book dataset.
- `books.json` – JSON-formatted book dataset.
- `summary_report.txt` – Summary statistics, including total books, average price, highest price, lowest price, and rating distribution.

## Learning Outcomes
- Understanding web scraping and HTML parsing.
- Implementing ETL workflows.
- Working with structured data formats.
- Handling HTTP errors and retries.
- Generating automated analytical reports.

## Author
Satheeswari

Python Software Engineering Internship – RabTech Academy