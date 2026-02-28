from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Ensure app folder is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.inference import neuroprana_inference

app = FastAPI(title="NeuroPrana API", version="1.0")

# your routes ...
from mangum import Mangum
handler = Mangum(app)

# -----------------------------
# Request Schema
# -----------------------------
class StressInput(BaseModel):
    stress_score: float
    positive_affect: float
    negative_affect: float
    clarity_rating: float
    age_band: str
    prior_adherence: float
    prior_delta: float


# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "NeuroPrana API is running."}


# -----------------------------
# Prediction Endpoint
# -----------------------------
@app.post("/predict")
def predict(data: StressInput):
    input_dict = data.dict()
    try:
        result = neuroprana_inference(input_dict)
        return result
    except Exception as e:
        return {"error": str(e)}
    
