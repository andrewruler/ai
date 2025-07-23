import requests
import re
import csv
import json
import time
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional

class TestContactScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        
    def extract_contact_info(self, html_content: str, url: str) -> Dict[str, str]:
        """Extract contact information from HTML content."""
        contact_info = {
            'emails': [],
            'phones': [],
            'contact_links': []
        }
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html_content, re.IGNORECASE)
        contact_info['emails'] = list(set([email.lower() for email in emails]))
        
        # Extract phone numbers (various formats)
        phone_patterns = [
            r'\+?1?\s*\(?[0-9]{3}\)?[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}',  # (123) 456-7890
            r'\+?[0-9]{1,4}[\s.-]?[0-9]{3,4}[\s.-]?[0-9]{3,4}',      # International
            r'1-800-[0-9]{3}-[0-9]{4}',                              # 1-800-XXX-XXXX
            r'1-888-[0-9]{3}-[0-9]{4}',                              # 1-888-XXX-XXXX
            r'1-877-[0-9]{3}-[0-9]{4}',                              # 1-877-XXX-XXXX
            r'[0-9]{3}[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}'               # 123-456-7890
        ]
        
        phones = []
        for pattern in phone_patterns:
            found_phones = re.findall(pattern, html_content)
            phones.extend(found_phones)
        contact_info['phones'] = list(set(phones))
        
        # Find contact links using regex
        contact_link_pattern = r'href=["\']([^"\']*(?:contact|about|support|help|reach)[^"\']*)["\']'
        contact_links = re.findall(contact_link_pattern, html_content, re.IGNORECASE)
        contact_info['contact_links'] = [urljoin(url, link) for link in contact_links]
        
        return contact_info
    
    def scrape_contact_page(self, url: str) -> Optional[Dict[str, str]]:
        """Scrape a specific contact page."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            return self.extract_contact_info(response.text, url)
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def find_contact_page(self, base_url: str) -> Optional[str]:
        """Try to find a contact page on the website."""
        try:
            response = self.session.get(base_url, timeout=15)
            response.raise_for_status()
            
            # Look for contact links in the HTML
            contact_link_pattern = r'href=["\']([^"\']*(?:contact|about|support|help|reach)[^"\']*)["\']'
            contact_links = re.findall(contact_link_pattern, response.text, re.IGNORECASE)
            
            if contact_links:
                # Return the first contact link found
                return urljoin(base_url, contact_links[0])
            
            # If no contact link found, return the base URL
            return base_url
            
        except Exception as e:
            print(f"Error finding contact page for {base_url}: {str(e)}")
            return None
    
    def process_company(self, company_name: str, existing_contact: str, website: str) -> Dict:
        """Process a single company to find contact information."""
        print(f"Processing: {company_name}")
        
        result = {
            'company_name': company_name,
            'existing_contact': existing_contact,
            'website': website,
            'scraped_emails': [],
            'scraped_phones': [],
            'contact_page_url': None,
            'status': 'pending'
        }
        
        if not website or website == 'N/A' or website == 'Not available':
            result['status'] = 'no_website'
            return result
        
        try:
            # Find contact page
            contact_page = self.find_contact_page(website)
            if contact_page:
                result['contact_page_url'] = contact_page
                
                # Scrape contact information
                contact_info = self.scrape_contact_page(contact_page)
                if contact_info:
                    result['scraped_emails'] = contact_info['emails']
                    result['scraped_phones'] = contact_info['phones']
                    result['status'] = 'success'
                else:
                    result['status'] = 'scrape_failed'
            else:
                result['status'] = 'no_contact_page'
                
        except Exception as e:
            result['status'] = 'error'
            print(f"Error processing {company_name}: {str(e)}")
        
        # Add delay to be respectful to servers
        time.sleep(2)
        
        return result
    
    def export_results(self, filename: str = 'test_contact_results.csv'):
        """Export results to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'company_name', 'existing_contact', 'website', 
                'scraped_emails', 'scraped_phones', 'contact_page_url', 'status'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.results:
                # Convert lists to strings for CSV
                row = result.copy()
                row['scraped_emails'] = '; '.join(result['scraped_emails'])
                row['scraped_phones'] = '; '.join(result['scraped_phones'])
                writer.writerow(row)
        
        print(f"Results exported to {filename}")
    
    def export_json(self, filename: str = 'test_contact_results.json'):
        """Export results to JSON file."""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.results, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Results exported to {filename}")

def main():
    # Test with just a few companies
    test_companies = [
        {
            'name': 'The Influence Agency',
            'contact': '(416) 254-2944 https://theinfluenceagency.com/contact',
            'website': 'https://theinfluenceagency.com/'
        },
        {
            'name': 'Scale',
            'contact': 'https://scale.com/contact-us',
            'website': 'https://scale.com/'
        },
        {
            'name': 'Genesys',
            'contact': 'https://www.genesys.com/contact-us',
            'website': 'https://www.genesys.com/'
        },
        {
            'name': 'LingYu',
            'contact': '(647) 728-2955 info@lingyupsyc.com',
            'website': 'https://www.lingyu.ca/'
        },
        {
            'name': 'OTT',
            'contact': 'https://ott.ca/contact/',
            'website': 'https://ott.ca/'
        }
    ]
    
    # Initialize scraper
    scraper = TestContactScraper()
    
    print("Starting test contact information scraping...")
    print("Processing 5 test companies...")
    
    # Process test companies
    for company in test_companies:
        result = scraper.process_company(
            company['name'],
            company['contact'],
            company['website']
        )
        scraper.results.append(result)
    
    # Export results
    scraper.export_results('test_contact_results.csv')
    scraper.export_json('test_contact_results.json')
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SCRAPING SUMMARY")
    print("="*50)
    
    status_counts = {}
    for result in scraper.results:
        status = result['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        print(f"{status}: {count} companies")
    
    print(f"\nTotal companies processed: {len(scraper.results)}")
    print("Check test_contact_results.csv and test_contact_results.json for detailed results")
    
    # Show some sample results
    print("\nSample results:")
    for result in scraper.results:
        print(f"\n{result['company_name']}:")
        print(f"  Status: {result['status']}")
        if result['scraped_emails']:
            print(f"  Emails found: {', '.join(result['scraped_emails'])}")
        if result['scraped_phones']:
            print(f"  Phones found: {', '.join(result['scraped_phones'])}")

if __name__ == "__main__":
    main() 