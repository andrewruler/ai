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
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='button'] span.css-1cehe4"))
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

def main():
    url = "https://www.wsj.com/politics/policy?mod=nav_top_subsection"
    driver = None
    try:
        driver = setup_driver()
        driver.get(url)
        logging.info(f"Loaded {url}")
        click_load_more(driver, max_clicks=None, wait_time=2)
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed.")

if __name__ == "__main__":
    main()
