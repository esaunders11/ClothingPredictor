import pickle
import pandas as pd

class resale_predictor:
    def __init__(self, platform):
        self.model = pickle.load(open('model/' + platform + '_XGB_price_model.pkl', 'rb'))
        self.columns = pickle.load(open('model/' + platform + '_model_features.pkl', 'rb'))

    def predict(self, brand=None, category=None, condition=None, size=None):
        brand = brand or "Unknown"
        category = category or "Unknown"
        condition = condition or "Pre-owned"
        size = size or "Unknown"

        input_data = pd.DataFrame([{
            "brand": brand,
            "category": category,
            "condition": condition,
            "size": size
        }])

        input_data = pd.get_dummies(input_data)

        input_data = input_data.reindex(columns=self.columns, fill_value=0)

        predicted_price = self.model.predict(input_data)[0]
        return round(float(predicted_price), 2)