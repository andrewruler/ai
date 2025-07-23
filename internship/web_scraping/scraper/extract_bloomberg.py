import pandas as pd
from selenium.webdriver.common.by import By

def extract_headlines_and_times(driver):
    print("Extracting headlines and times from the page...")
    results = []
    # Find all headline containers
    headline_blocks = driver.find_elements(
        By.CSS_SELECTOR, "a.styles_itemLink__VgyXJ"
    )
    print(f"Found {len(headline_blocks)} article blocks.")
    for block in headline_blocks:
        try:
            # Headline
            headline_elem = block.find_element(By.CSS_SELECTOR, "div.Headline_phoenix__Dvz0u.Headline_large__BPshg")
            headline = headline_elem.text.strip()

            # Find the closest time element by traversing up to the container, then down
            container = block.find_element(By.XPATH, "./ancestor::div[contains(@class, 'styles_itemContainer__t2ZQc')]")
            time_elem = container.find_element(By.CSS_SELECTOR, "time")
            time_text = time_elem.text.strip() if time_elem else ""

            results.append({
                "headline": headline,
                "time": time_text
            })
        except Exception:
            continue
    print(f"Extraction complete. {len(results)} headlines found.")
    return results

def save_headlines_and_times_to_csv(data, csv_path):
    print(f"Saving {len(data)} records to {csv_path} ...")
    df = pd.DataFrame(data)
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
    save_headlines_and_times_to_csv(data, "../data/headlines_bloomberg.csv")
    print(f"Saved {len(data)} headlines to ../data/headlines_bloomberg.csv")
    driver.quit()
    print("Browser session closed.")

if __name__ == "__main__":
    print("Script started.")
    attach_and_extract()
    print("Script finished.")