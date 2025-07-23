# Financial News Headlines Web Scraping Project

## Objective
Scrape ~2,500 unique financial news headlines per person (total 10,000), focusing on financial news that may affect stock movement.

## Data Sources
- **Bloomberg Markets:** https://www.bloomberg.com/markets
- **Wall Street Journal – Markets:** https://www.wsj.com/news/markets

## Timeframe
- Headlines from **Jan 1, 2022 – Dec 31, 2023** (extend if needed to reach headline target).

## Required Fields
- `headline`: Title of the news article
- `timestamp`: Publication date and time (UTC preferred)
- `source`: Website name (e.g., Yahoo Finance)
- `url`: Original link

## Project Structure

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/financial-news-scraper.git
   ```
2. **Activate the virtual environment:**
- Windows:
  ```
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```
  source venv/bin/activate
  ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add your configuration, e.g.:
     ```
     DATABASE_URL=your_database_url
     SECRET_KEY=your_secret_key
     ```
5. **Run the scraper:**
   ```
   python main.py
   ```
6. **Schedule regular runs (optional):**
   - Use `cron` jobs (Linux/macOS) or Task Scheduler (Windows) to run the scraper at regular intervals.

## Usage

- Run the main script to start scraping:
- Scraped data will be saved in the `data/` directory as CSV files.

## Notes

- Respect each website's robots.txt and terms of service.
- Add delays between requests to avoid overloading servers.
- Ensure deduplication of headlines.
- If the specified timeframe does not yield enough headlines, extend the date range as needed.

## To Do

- Implement scrapers for Bloomberg and WSJ in `scraper/`.
- Add data validation and deduplication in `utils.py`.
- Combine and analyze data as needed.
