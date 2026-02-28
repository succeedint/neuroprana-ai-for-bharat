from fastapi import FastAPI, HTTPException
import joblib
import os
import pandas as pd
import boto3
import json

# Load model once at cold start
MODEL_PATH = os.path.join(os.path.dirname(__file__), "neuroprana_random_forest_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Model loading failed: {e}")

app = FastAPI()
# Initialize Bedrock client (IAM role recommended)
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)
def build_prompt(data, prediction, protocol):
    return f"""
A user has the following indicators:

Stress score: {data['stress_score']}
Negative affect: {data['negative_affect']}
Clarity rating: {data['clarity_rating']}

Predicted stress state: {prediction}.
Recommended protocol: {protocol['protocol_name']}.

Generate a short, supportive, non-medical explanation in 3 sentences.
Do not diagnose.
Do not provide medical advice.
Keep tone calm and reassuring.
"""


def call_bedrock(prompt):
    try:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "temperature": 0.3,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:us-east-1:311493921100:inference-profile/us.anthropic.claude-sonnet-4-6",
            body=json.dumps(body)
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"]

    except Exception as e:
        print("Bedrock error:", e)
        return None


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

        # Protocol selection
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

        # Build Bedrock prompt
        prompt = build_prompt(data, prediction, protocol)
        llm_explanation = call_bedrock(prompt)

        # Fallback if Bedrock fails
        if not llm_explanation:
            llm_explanation = (
                "Your current indicators suggest changes in stress level. "
                "A structured breathing practice may help support emotional balance."
            )

        return {
            "predicted_stress_state": str(prediction),
            "recommended_protocol": protocol,
            "explanation": llm_explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))