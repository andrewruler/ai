from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import pandas as pd
import os

# Set up logging
logging.basicConfig(
    filename='../logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def click_load_more(driver, max_clicks=None, wait_time=2):
    """
    Scroll and click 'Load More' button until it's no longer available or max_clicks is reached.
    """
    clicks = 0
    while True:
        if max_clicks and clicks >= max_clicks:
            logging.info(f"Reached maximum number of clicks: {max_clicks}")
            break
        try:
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            # Wait for the Load More button
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'media-ui-Button_text-N76nbJyFyw0-') and contains(text(), 'Load more')]"))
            )
            # Click the button
            button.click()
            clicks += 1
            logging.info(f"Clicked Load More button {clicks} times")
            time.sleep(wait_time)
        except TimeoutException:
            logging.info("No more 'Load More' button found. Stopping.")
            break
        except Exception as e:
            logging.error(f"Error during clicking: {str(e)}")
            break

def extract_articles(driver):
    """
    Dummy extractor for Bloomberg. You need to update selectors based on the actual Bloomberg article structure.
    """
    articles = []
    # Example: Find all headline elements (update selector as needed)
    headline_blocks = driver.find_elements(By.CSS_SELECTOR, "a[data-tracking-type='headline']")
    for headline_elem in headline_blocks:
        try:
            headline = headline_elem.text.strip()
            url = headline_elem.get_attribute("href")
            # Dummy placeholders for authors and date (update as needed)
            authors = ""
            date = ""
            articles.append({
                "headline": headline,
                "authors": authors,
                "date": date,
                "url": url
            })
        except Exception as e:
            logging.error(f"Error extracting article: {str(e)}")
            continue
    return articles

def main():
    # Open the Bloomberg Markets page in your debug Chrome before running
    driver = None
    try:
        driver = setup_driver()
        logging.info("Attached to existing Chrome session.")
        time.sleep(3)  # Let page load if needed

        click_load_more(driver, wait_time=2)
        time.sleep(2)  # Wait for last articles to load

        articles = extract_articles(driver)
        logging.info(f"Extracted {len(articles)} articles.")

        # Save to CSV
        os.makedirs("../data", exist_ok=True)
        df = pd.DataFrame(articles)
        df.to_csv("../data/headlines_bloomberg.csv", index=False)
        print(f"Saved {len(df)} articles to ../data/headlines_bloomberg.csv")

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed.")

if __name__ == "__main__":
    main()