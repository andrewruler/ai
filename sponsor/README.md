# Contact Information Scraper

This tool automates the process of finding contact information (emails, phone numbers, contact pages) from company websites.

## Features

- **Automated Web Scraping**: Scrapes company websites to find contact information
- **Email Detection**: Uses regex patterns to find email addresses
- **Phone Number Detection**: Supports multiple phone number formats (North American, international)
- **Contact Page Discovery**: Automatically finds contact/about pages on websites
- **Multiple Export Formats**: Exports results to CSV and JSON
- **Respectful Scraping**: Includes delays between requests to be respectful to servers

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the scraper:
```bash
python contact_scraper.py
```

2. The script will:
   - Process all companies from the provided data
   - Scrape their websites for contact information
   - Export results to `contact_results.csv` and `contact_results.json`

## Output Files

### contact_results.csv
Contains the following columns:
- `company_name`: Name of the company
- `existing_contact`: Contact information already provided
- `website`: Company website URL
- `scraped_emails`: List of email addresses found
- `scraped_phones`: List of phone numbers found
- `contact_page_url`: URL of the contact page found
- `status`: Processing status (success, error, no_website, etc.)

### contact_results.json
Same data in JSON format for programmatic access.

## Status Codes

- `success`: Successfully scraped contact information
- `no_website`: No website provided
- `no_contact_page`: Could not find contact page
- `scrape_failed`: Failed to scrape the contact page
- `error`: General error occurred
- `pending`: Not yet processed

## Customization

To process different companies, modify the `data` variable in the `main()` function of `contact_scraper.py`.

## Notes

- The scraper includes a 1-second delay between requests to be respectful to web servers
- Some websites may block automated requests
- Results may vary depending on website structure and anti-bot measures
- Always respect robots.txt and website terms of service

## Legal Notice

This tool is for educational and legitimate business purposes only. Always:
- Respect website terms of service
- Check robots.txt files
- Use reasonable request rates
- Only scrape publicly available information 