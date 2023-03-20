from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time



def search(term, pages:int=10, sleep_interval: int=1):
    path = Path(".\chromedriver.exe")
    if not path.exists():
        print(f"Chrome driver does not exist at {path}, please download to use Selenium")

    driver = webdriver.Chrome(executable_path=".\chromedriver.exe")
    driver.implicitly_wait(0.5)

    driver.get("https://www.google.com/")
    # Find search box
    search_box = driver.find_element(by=By.NAME, value="q")
    search_box.send_keys(term)
    time.sleep(0.2)
    search_box.send_keys(Keys.ENTER)

    links = []

    # Scan first page then move on
    soup = BeautifulSoup(driver.page_source, "lxml")
    for a in soup.find_all('a', href=True):
        if a['href'].startswith("https://play.google.com") :
            links.append(a['href'])

    for _ in range(pages):
        try:
            # Try to click "More results" button
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".T7sFge"))).click()
        except Exception:
            pass

        # Scroll the page then sleep
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_interval)
        
        # Append the new urls
        soup = BeautifulSoup(driver.page_source, "lxml")
        for a in soup.find_all('a', href=True):
            if a['href'].startswith("https://play.google.com") :
                links.append(a['href'])

    return links