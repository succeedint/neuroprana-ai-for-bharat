from fastapi import FastAPI, HTTPException
import joblib
import os
import pandas as pd

# Load model once at cold start
MODEL_PATH = os.path.join(os.path.dirname(__file__), "neuroprana_random_forest_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Model loading failed: {e}")

app = FastAPI()


@app.get("/")
def root():
    return {"message": "NeuroPrana Cloud API Running"}


@app.post("/predict")
def predict(data: dict):

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # Convert JSON payload to DataFrame
        input_df = pd.DataFrame([{
            "stress_score": data["stress_score"],
            "positive_affect": data["positive_affect"],
            "negative_affect": data["negative_affect"],
            "clarity_rating": data["clarity_rating"],
            "adherence_rate": data["adherence_rate"],
            "prior_delta": data["prior_delta"],
            "age_band": data["age_band"],
            "prior_adherence": data["prior_adherence"]
        }])

        # Run prediction
        prediction = model.predict(input_df)[0]

        # Basic protocol logic (you can refine later)
        if prediction == "High":
            protocol = {
                "protocol_name": "Calming Breath (Slow Diaphragmatic)",
                "duration_minutes": 5,
                "cadence": "4-6 breathing",
                "goal": "Reduce sympathetic activation and calm stress response"
            }
        elif prediction == "Moderate":
            protocol = {
                "protocol_name": "Balanced Breath (Box Breathing)",
                "duration_minutes": 4,
                "cadence": "4-4-4-4",
                "goal": "Stabilize emotional state and improve clarity"
            }
        else:
            protocol = {
                "protocol_name": "Energizing Breath (Stimulating)",
                "duration_minutes": 3,
                "cadence": "Active inhale emphasis",
                "goal": "Enhance alertness and positive activation"
            }

        return {
            "predicted_stress_state": str(prediction),
            "recommended_protocol": protocol,
            "explanation": f"Model predicted '{prediction}' stress state based on provided inputs."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
