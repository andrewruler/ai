from selenium import webdriver
from config.settings import SELENIUM_DRIVER_PATH

def get_driver():
    """Initialize and return a Selenium WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without UI
    options.add_argument("--disable-blink-features=AutomationControlled")  # Reduce bot detection
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(executable_path=SELENIUM_DRIVER_PATH, options=options)
    driver.implicitly_wait(10)
    return driver
