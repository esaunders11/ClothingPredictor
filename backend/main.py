import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.resale_predictor import resale_predictor


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ebay_predictor = resale_predictor("ebay")
poshmark_predictor = resale_predictor("poshmark")

class PredictionRequest(BaseModel):
    brand: str
    category: str
    condition: str
    size: str
    platform: str

@app.post("/predict")
def predict_price(req: PredictionRequest):
    if req.platform.lower() == "ebay":
        return ebay_predictor.predict(req.brand, req.category, req.condition, req.size)
    elif req.platform.lower() == "poshmark":
        return poshmark_predictor.predict(req.brand, req.category, req.condition, req.size)
    else:
        return {"error": "Unsupported platform"}