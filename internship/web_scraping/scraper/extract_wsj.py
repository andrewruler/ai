import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_headlines_and_times(driver):
    """
    Extracts headlines and times from the WSJ page using updated selectors.
    """
    print("Waiting for page to load headlines...")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='flexcard-headline'] div"))
        )
        print("Headline elements appeared (wait successful).")
    except Exception as e:
        print("Timeout or error while waiting for headline elements!")
        print("Exception:", e)
        print("Page title:", driver.title)
        print("Current URL:", driver.current_url)
        print("Dumping first 500 chars of page source for inspection:")
        print(driver.page_source[:500])
        return []

    # Optional: Scroll to the bottom to load more headlines
    print("Scrolling to bottom of page...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    print("Extracting headlines and times from the page...")
    results = []
    headline_blocks = driver.find_elements(By.CSS_SELECTOR, "[data-testid='flexcard-headline'] div")
    print("Found headline blocks:", len(headline_blocks))

    for i, block in enumerate(headline_blocks):
        try:
            headline = block.text.strip()
            print(f"Headline {i+1}: {headline[:60]}")
            # Traverse to parent card and get the timestamp
            card_container = block.find_element(By.XPATH, "./ancestor::div[contains(@class, 'e1u7xa1g1')]")
            time_elem = card_container.find_element(By.CSS_SELECTOR, "p[data-testid='timestamp-text']")
            time_text = time_elem.text.strip() if time_elem else ""
            print(f"  Time: {time_text}")
            results.append({
                "headline": headline,
                "time": time_text
            })
        except Exception as e:
            print(f"Error extracting for block {i+1}: {block.text[:30]}... | {e}")
            continue

    print(f"Extraction complete. {len(results)} headlines found.")
    return results

def save_headlines_and_times_to_csv(data, csv_path):
    print(f"Saving {len(data)} records to {csv_path} ...")
    df = pd.DataFrame(data)
    print(df.head())  # Show sample
    if "headline" not in df.columns or "time" not in df.columns:
        print("ERROR: Extracted data missing required columns.")
        return
    df.to_csv(csv_path, index=False, columns=["headline", "time"])
    print("Save complete.")

def attach_and_extract():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    print("Attaching to existing Chrome session...")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("Starting extraction process...")
    data = extract_headlines_and_times(driver)
    save_headlines_and_times_to_csv(data, "../data/headlines_wsj.csv")
    print(f"Saved {len(data)} headlines to ../data/headlines_wsj.csv")
    driver.quit()
    print("Browser session closed.")

if __name__ == "__main__":
    print("Script started.")
    attach_and_extract()
    print("Script finished.")
