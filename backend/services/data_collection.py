import re
import pandas as pd
from glob import glob
from backend.scrapers.ebay_scraper import scrape_ebay
from backend.scrapers.poshmark_scraper import scrape_poshmark

def load_and_standardize(file):
    df = pd.read_csv(file)

    standard_columns = [
        "title", "brand", "category", "sub_category", "condition",
        "size", "sell_price", "platform"
    ]

    df = df[standard_columns]
    return df

def merge_platform_files(files, output_file):
    dfs = [load_and_standardize(f) for f in files]
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.drop_duplicates(subset=["title", "platform"], inplace=True)
    combined_df["brand"] = combined_df["brand"].str.strip().str.title()
    combined_df["condition"] = combined_df["condition"].str.lower().str.capitalize()
    combined_df.to_csv(output_file, index=False)
    return combined_df

def merge_scraped_data():
    ebay_df = merge_platform_files(
        glob("backend/data/raw/ebay_*_listings.csv"),
        "backend/data/processed/ebay_listings.csv"
    )
    poshmark_df = merge_platform_files(
        glob("backend/data/raw/poshmark_*_listings.csv"),
        "backend/data/processed/poshmark_listings.csv"
    )

    print("Merged data summary:")
    print(poshmark_df["platform"].value_counts())
    print(ebay_df["platform"].value_counts())
    print(f"Total listings: eBay: {len(ebay_df)}, Poshmark: {len(poshmark_df)}")

def scrape_data(search):
    ebay_df = scrape_ebay(search)
    poshmark_df = scrape_poshmark(search)
    query_name = re.sub(r"[^a-zA-Z0-9_]", "_", search.strip().lower())
    if not ebay_df.empty:
        ebay_df.to_csv(f"backend/data/raw/ebay_{query_name}_listings.csv", index=False)
    if not poshmark_df.empty:
        poshmark_df.to_csv(f"backend/data/raw/poshmark_{query_name}_listings.csv", index=False)


if __name__ == "__main__":
    inputs = ["nike hoodie", "north face fleece", "nike dunk", "adidas samba", "puffer jacket", "patagonia down jacket", "mens slacks", "college quarterzip"]
    # for search in inputs:
    #     scrape_data(search)
    merge_scraped_data()
