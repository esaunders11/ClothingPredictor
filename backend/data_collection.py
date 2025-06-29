import re
import pandas as pd
from glob import glob
from ebay_scraper import scrape_ebay
from poshmark_scraper import scrape_poshmark

def load_and_standardize(file):
    df = pd.read_csv(file)

    standard_columns = [
        "title", "brand", "category", "condition",
        "size", "sell_price", "platform"
    ]

    df = df[standard_columns]
    return df

def merge_scraped_data():
    files = glob("backend/data/raw/*_listings.csv")
    dfs = [load_and_standardize(f) for f in files]
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.drop_duplicates(subset=["title", "platform"], inplace=True)

    combined_df["brand"] = combined_df["brand"].str.strip().str.title()
    combined_df["condition"] = combined_df["condition"].str.lower().str.capitalize()

    combined_df.to_csv("backend/data/processed/listings.csv", index=False)

    print("Merged data summary:")
    print(combined_df["platform"].value_counts())
    print(f"Total listings: {len(combined_df)}")

def scrape_data(search):
    ebay_df = scrape_ebay(search)
    #poshmark_df = scrape_poshmark(search)
    query_name = re.sub(r"[^a-zA-Z0-9_]", "_", search.strip().lower())
    if not ebay_df.empty:
        ebay_df.to_csv(f"backend/data/raw/ebay_{query_name}_listings.csv", index=False)
    # if not poshmark_df.empty:
    #     poshmark_df.to_csv(f"backend/data/raw/poshmark_{query_name}_listings.csv", index=False)


if __name__ == "__main__":
    inputs = ["graphic tee", "carhart jacket", "nike air jordan", "athletic jacket", "college shirt", "collard shirt", "leather jacket", "winter jacket", "streetwear tee", 
              "vintage band tee", "vintage denim jeans",]
    for search in inputs:
        scrape_data(search)
    merge_scraped_data()
