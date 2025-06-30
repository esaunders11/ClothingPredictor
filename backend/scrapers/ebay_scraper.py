import requests
from bs4 import BeautifulSoup
import pandas as pd
from backend.services.TitleExtractor import TitleExtractor
import time

def scrape_ebay(query):
    base_url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "+") + "&rt=nc&LH_Sold=1&LH_Complete=1&_pgn="

    title_extractor = TitleExtractor()
    data = []

    for page in range(1, 21):
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select('.s-item')
        print(f"Found {len(items)} items on page {page}")
        for item in items:
            try:
                title_elem = item.select_one('.s-item__title')
                price_elem = item.select_one('.s-item__price')
                condition_elem = item.select_one('.SECONDARY_INFO')

                if not title_elem or not price_elem:
                    continue

                title = title_elem.text.strip()
                price = price_elem.text.strip().replace('$', '').replace(',', '')
                condition = condition_elem.text.strip() if condition_elem else "Unknown"

                info = title_extractor.extract_fields(title)

                data.append({
                    "title": title,
                    "brand": info["brand"],
                    "category": info["category"],
                    "sub_category": info["sub_category"],
                    "condition": condition,
                    "size": info["size"],
                    "sell_price": float(price) if price.replace('.', '', 1).isdigit() else None,
                    "platform": "eBay"
                })
            except Exception as e:
                print(f"Skipping listing due to error: {e}")
                continue
        time.sleep(1)

    df = pd.DataFrame(data)
    return df

