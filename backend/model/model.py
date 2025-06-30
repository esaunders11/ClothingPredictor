import pandas as pd
import pickle
import re
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor

def clean_data(df):
    df["sell_price"] = pd.to_numeric(df["sell_price"], errors="coerce")
    df = df.dropna(subset=["sell_price"])
    df = df[df["sell_price"] > 0]

    price_cap = df["sell_price"].quantile(0.95)
    df = df[df["sell_price"] <= price_cap]

    df["size_normalized"] = df["size"].apply(normalize_size)

    df["brand"] = df["brand"].fillna("Unknown").str.strip().str.lower().str.title()
    brand_avg_price = df.groupby("brand")["sell_price"].mean()
    df["brand_encoded"] = df["brand"].map(brand_avg_price).fillna(df["sell_price"].mean())
    
    df["condition"] = df["condition"].str.lower().str.strip()
    df["condition"] = df["condition"].apply(lambda x: "New" if "new" in x else "Pre-owned")

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df = df.drop_duplicates(subset=["title", "platform"])

    return df

def normalize_size(size):
    size = str(size).strip().upper()

    letter_size_map = {
    "XXS": "XS", "Extra Small": "XS", "XS": "XS",
    "Small": "S", "S": "S",
    "Medium": "M", "M": "M",
    "Large": "L", "L": "L",
    "Extra Large": "XL", "XL": "XL", "XXL": "XXL", "2XL": "XXL"
    }

    if size in letter_size_map:
        return letter_size_map[size]
    match = re.search(r'\b(\d{1,2})(?:X\d{1,2})?\b', size)
    if match:
        num = int(match.group(1))
        if num <= 28:
            return "XS"
        elif 29 <= num <= 30:
            return "S"
        elif 31 <= num <= 32:
            return "M"
        elif 33 <= num <= 34:
            return "L"
        elif 35 <= num <= 36:
            return "XL"
        else:
            return "XXL"
    
    return "Unknown"
    
def create_model(platform):
    platform = platform.strip().lower()
    df = pd.read_csv("backend/data/processed/" + platform + "_listings.csv")
    df = clean_data(df)
    print(df.head())
    print(df["sell_price"].mean())

    x = df[["brand_encoded", "category", "sub_category", "condition", "size_normalized"]]
    y = df["sell_price"]

    x = pd.get_dummies(x)
    with open("backend/model/" + platform + "_model_features.pkl", "wb") as f:
        pickle.dump(x.columns.tolist(), f)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    params = {
        'n_estimators': [100, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.05, 0.1, 0.2]
    }

    model = GridSearchCV(XGBRegressor(), param_grid=params, cv=5, scoring='neg_mean_absolute_error')
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Mean absolute error XGB: ${mae:.2f}")

    # rf = RandomForestRegressor(n_estimators=300, random_state=42)
    # rf.fit(x_train, y_train)
    # rf_preds = rf.predict(x_test)
    # rf_mae = mean_absolute_error(y_test, rf_preds)
    # print(f"Mean absolute error RF: ${rf_mae:.2f}")

    # with open("backend/model/RFR_price_model.pkl", "wb") as file:
    #     pickle.dump(rf, file)
    with open("backend/model/" + platform + "_XGB_price_model.pkl", "wb") as file:
        pickle.dump(model, file)

create_model("ebay")
create_model("poshmark")
