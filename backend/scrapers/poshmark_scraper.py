import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from backend.services.TitleExtractor import TitleExtractor
import time

def scrape_poshmark(query, max_scrolls=10):
    url = "https://poshmark.com/search?query=" + query.replace(" ", "%20") + "&availability=sold_out"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    title_extractor = TitleExtractor()
    data = []

    items = driver.find_elements(By.CLASS_NAME, "card")
    print(f"Found {len(items)}")
    for i in range(len(items)):
        try:
            items = driver.find_elements(By.CLASS_NAME, "card")
            item = items[i]
            title_elem = item.find_element(By.CSS_SELECTOR, '.title__condition__container')
            price_elem = item.find_element(By.CSS_SELECTOR, '.p--t--1')
            details_div = item.find_element(By.CSS_SELECTOR, '.d--fl.m--t--1')
            try:
                details_div = item.find_element(By.CSS_SELECTOR, '.d--fl.m--t--1')

                brand_elems = details_div.find_elements(By.CSS_SELECTOR, '.tile__details__pipe__brand.ellipses')
                size_elems = details_div.find_elements(By.CSS_SELECTOR, '.tile__details__pipe__size.ellipses')

                brand = brand_elems[0].text.strip() if brand_elems else "Unknown"
                size = size_elems[0].text.strip() if size_elems else "Unknown"

            except Exception as e:
                print("Skipping: failed to extract brand/size:", e)
                brand = "Unknown"
                size = "Unknown"

            title = title_elem.text.strip()
            price = price_elem.text.strip().replace('$', '').replace(',', '')

            info = title_extractor.extract_fields(title + " " + size)

            data.append({
                "title": title,
                "brand": brand,
                "category": info["category"],
                "sub_category": info["sub_category"],
                "condition": "pre-owned",
                "size": info["size"],
                "sell_price": float(price) if price.replace('.', '', 1).isdigit() else None,
                "platform": "Poshmark"
            })
        except Exception as e:
            print(f"Skipping listing due to error: {e}")
            continue
    time.sleep(1)

    driver.quit()
    df = pd.DataFrame(data)
    return df


