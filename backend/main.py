import pandas as pd
from ebay_scraper import scrape_ebay

df = scrape_ebay("band tees")
df.to_csv("test_data.csv", index=False)