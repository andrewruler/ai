import requests
import re
import csv
import json
import time
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional

class SimpleContactScraper:
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
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return self.extract_contact_info(response.text, url)
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def find_contact_page(self, base_url: str) -> Optional[str]:
        """Try to find a contact page on the website."""
        try:
            response = self.session.get(base_url, timeout=10)
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
        time.sleep(1)
        
        return result
    
    def process_companies_from_data(self, data_text: str) -> List[Dict]:
        """Process companies from the provided data text."""
        lines = data_text.strip().split('\n')
        companies = []
        
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 3:
                    company_name = parts[0].strip()
                    existing_contact = parts[1].strip()
                    website = parts[2].strip()
                    
                    companies.append({
                        'name': company_name,
                        'contact': existing_contact,
                        'website': website
                    })
        
        results = []
        for company in companies:
            result = self.process_company(
                company['name'],
                company['contact'],
                company['website']
            )
            results.append(result)
            self.results.append(result)
        
        return results
    
    def export_results(self, filename: str = 'simple_contact_results.csv'):
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
    
    def export_json(self, filename: str = 'simple_contact_results.json'):
        """Export results to JSON file."""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.results, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Results exported to {filename}")

def main():
    # Your data
    data = """Company Name	Contact Email/Number/Website Contact	Website	Appearance 
Adobe	N/A	https://www.adobe.com/ca/	
The Influence Agency	(416) 254-2944 https://theinfluenceagency.com/contact	https://theinfluenceagency.com/  	
Manulife	 1-866-318-2727	https://www.manulife.ca/personal.html	
Scale	https://scale.com/contact-us	https://scale.com/	
Genesys	https://www.genesys.com/contact-us	https://www.genesys.com/	
Royal Bank of Canada	1 (800) 769-2511	https://www.rbcroyalbank.com/personal.html	
Re/Max	437-838-8111	https://www.remax.ca/	
LingYu	(647) 728-2955 info@lingyupsyc.com	https://www.lingyu.ca/	
OTT	https://ott.ca/contact/	https://ott.ca/	
CIBC	1 (800) 465-2422	https://www.cibc.com/en/personal-banking.html	2
Al Premium	https://alpremium.ca/pages/contactus	https://alpremium.ca/	
Maxperr	https://maxperrenergy.com/collaboration/	https://maxperrenergy.com/	
Scotiabank	https://www.scotiabank.com/ca/en/personal/contact-us.html	https://www.scotiabank.com/ca/en/personal.html	3
CarBest	 (905) 294-6999. https://www.carbest.ca/contact-us/	https://www.carbest.ca/	
Academy of Learning	 info@aoltoronto.com (email)	https://www.academyoflearning.com/.	
Leaf Filter	1-800-290-6106	https://www.leaffilter.com/ 	
Noic Academy	 (416) 291-8829	https://noic.ca/	
Young Science	(647) 383-6931	https://youthscience.ca/	
Will and CO Fitness Studio	https://www.willcofit.com/contact	https://www.willcofit.com/	
Wellcare Insurance Corp	(905) 234-6666. https://wellcareinsurance.ca/contact/	https://wellcareinsurance.ca/	
Chat Insurance	https://chatin.ca/contact-us/	https://chatin.ca/	
Ontario College of Traditional Chinese Medicine	"T. 416 901 8818

E. toronto@octcm.com"	https://www.octcm.com/	
Family Holidays	 (416) 800-7043	https://familyholiday.ca/	
Hua Men Trading	 (416) 644-2995	https://j-k-house.myshopify.com/	
Hai Di Lao	604-370-6665	https://www.haidilao-inc.com/ca	
DeRucci	(905) 477-8777	https://derucci.ca/en/	2
Constant Home COmfort	https://constanthomecomfort.com/contacts/	https://constanthomecomfort.com/	
Seven Noodles	(416) 992-1203	N/A	
Chahalo	(437) 660-2222	https://cha-halo.ca/	
Hungry Panda	Business@hungrypanda.co	https://www.hungrypanda.co/	
Cha Bunny	(437) 733-0766	N/A	2
Flower Bunny	437-733-0766	N/A	2
Shanxi Association of Toronto	647-709-9591	https://www.sxaoc.ca/	
Results Advertising	(647) 930-3284	https://www.resultstoronto.com/	
TCCSA	"Live Chat: TCCSA website
Telephone: (416) 977-4026
Fax: (416) 351-0510
Email: info@tccsa.org"	https://tccsa.on.ca/	
Cocomax	66 2073 0977 and +66 2722 9389	https://www.cocomax.com/qr	
STMG	info@stmg.ca	https://www.stmg.ca/RONA.html	
鲤鱼传媒			4
Wukong	628-358-9588	https://www.wukongsch.com/	2
4	Email：feedback@fantuan.ca 	https://www.fantuan.ca/en/	3
777 Stone	(905) 478-8881	https://www.777stone.com/	
LingoAce	support@lingoace.zohodesk.com	https://www.lingoace.com/	
Fotile	(905) 604-8996	https://us.fotileglobal.com/?srsltid=AfmBOooxL3SzuKwhRAncL77gDc0xh1ArfX4aab7-HTkCROrLlaVN6z8d	
Lemfi	437-500-1260	https://lemfi.com/en-ca/	
DealMoon	katherine.capell@dealmoon.com	https://www.dealmoon.ca/	
iQiYi	ir@qiyi.com	https://m.iqiyi.com/	4
Eventgo	https://eventgo.ca/contact	https://eventgo.ca/	
Virgo	support@virgo.co	https://virgo.co/	
Aquavie	N/A	https://aquavie.ca/password	
Audemus Law Firm	alf@audemuslaw.com	https://www.xsunlaw.com/	
XS Law	xin@xsunlaw.com or info@xsunlaw.com	https://www.xsunlaw.com/	
InsMax	(905) 479-3888	https://www.insmaxbeautylounge.com/	3
Ali Travel	(647) 689-6888	https://superalitravel.com/	2
Dragon Pearl 	 (647) 348-7886	https://www.dragonpearlbuffet.com/	
NoFrills	https://www.nofrills.ca/en/contact-us	https://www.nofrills.ca/en	
T&T	https://www.tntsupermarket.com/contactus	https://www.tntsupermarket.com/eng/	2
Sukoshi	https://sukoshi.com/pages/contact-us	https://sukoshi.com/	
BizPop	(647) 283-4582	https://thebizpop.com/	
Sunshine Party and Tent Rentals	(416) 546-4506	https://sunshinepartyrentals.ca/	
Represent Asian Project	info@representasianproject.com	https://representasianproject.com/	
MCF Family Office	(855)940-8887	https://mcffo.ca/	
TS MCN (北美TS社美MCN)	N/A	N/A	
Fruya Arts & Culture	Email: fruya.culture@gmail.com | Instagram: @fruya.ca	https://www.fruya.ca	
星多多 (StarDuoDuo)	N/A	N/A	
彩龙文化	N/A	N/A	
飘雪奖	N/A	N/A	
Husky Media	N/A	N/A	
星悦传媒	N/A	N/A	
SG颁奖 (SG Awards)	N/A	N/A	
加拿大新生活报	N/A	https://newlifepost.ca	
加拿大家长帮	N/A	N/A	
中文电视	N/A	N/A	
华人头条 (Chinese Headline News)	Email: info@chinesenewsvideo.com	https://chineseheadline.ca	
华人生活馆	N/A	N/A	
活动加 (EventPlus)		N/A	
CCCTV 北美	Canada Chinese Community TV – info@ccctv.ca	https://ccctv.ca	
Kankan News	N/A	https://www.kankanews.com	
Legends 传媒	N/A	N/A	
微播中国	N/A	N/A	
侨华网	Chinese-Canadian news portal	https://www.chinesepress.com/	
UTSC CSSA	Instagram: @utsccssa | Bilibili UID: 413595919	N/A	
Easy Transfer (ET思汇)	N/A	N/A	
TYS International (信雅国际)	N/A	https://tysxinya.com/	
CheersYou Education (青椰教育)	N/A	https://www.cheersyou.com/en	
R Spa	(905) 479-3366	https://www.rspa.ca/	
China Southern Airlines (中国南方航空)	N/A	https://www.csair.com	
Utopia Marketing	info@utopiamarketing.ca | +1 647-223-3326	https://www.utopiamarketing.ca/	
MetroSquare	3636 Steeles Ave E, Markham, ON | Leasing: 905-940-3636 | Events: 437-998-7003	https://metrosquare.ca/	
Maple Waves	Not available	Not available	
Fairchild Radio (AM1430)	905-415-1430	https://www.am1430.com/	
Fairchild TV (新時代電視)	Not available	https://www.fairchildtv.com/	
Ontario SPCA	info@ontariospca.ca	https://ontariospca.ca/	
City of Toronto	311@toronto.ca | 311 (within city)	https://www.toronto.ca/	
Sharon He	647 280-6171| he_sharon@hotmail.com	https://www.citistarfinancial.com/	
NOVA Scientia	associate.clubs@westernusc.ca	https://club-spotlight.ca/nova-scientia/	
TOP Offer	Not available	https://www.topoffer.ca/	
ED-Venturelist	Not available	Not available	
Empower International Education	Not available	Not available	
Hello Tomato	Not available	Not available	
Snaplii	info@snaplii.com	https://www.snaplii.com	
BMO (Bank of Montreal)	1-877-225-5266	https://www.bmo.com	
Pepper Wireless	support@pepperwireless.ca	https://www.pepperwireless.ca	
Fido	1-888-481-3436	https://www.fido.ca	
Hi Yogurt	Not available	Not available	
Belong Education	Not available	Not available	
BORU Asian Cuisine	Not available	https://www.boruasian.com	
方华家具	Not available	Not available	
Kung Fu Tea	info@kungfuteatoronto.com	https://www.kungfuteatoronto.com	
Gol's Lanzhou Noodle	info@golsnoodle.com	https://www.golsnoodle.com	
糖甜记 Sugar Marmalade	Not available	https://sugarmarmalade.com	
EAR Home Service	Not available	Not available	
Panda BBQ	Not available	Not available	
Berrydream	Not available	Not available	
锦鲤 Sushi Koi	Not available	https://www.sushikoi.ca	
EZPass Driving School	ezpassschool@gmail.com	https://ezpassdrivingschool.ca	
REMIX KTV	remixktv@gmail.com	https://www.remixktv.ca	
Oplaza Sushi	Not available	https://oplaza.ca"""
    
    # Initialize scraper
    scraper = SimpleContactScraper()
    
    print("Starting simple contact information scraping...")
    print("This may take a while as we process each company website...")
    
    # Process all companies
    results = scraper.process_companies_from_data(data)
    
    # Export results
    scraper.export_results('simple_contact_results.csv')
    scraper.export_json('simple_contact_results.json')
    
    # Print summary
    print("\n" + "="*50)
    print("SCRAPING SUMMARY")
    print("="*50)
    
    status_counts = {}
    for result in results:
        status = result['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        print(f"{status}: {count} companies")
    
    print(f"\nTotal companies processed: {len(results)}")
    print("Check simple_contact_results.csv and simple_contact_results.json for detailed results")

if __name__ == "__main__":
    main() 