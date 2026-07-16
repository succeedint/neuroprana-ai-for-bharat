from fastapi import FastAPI, HTTPException
import joblib
import os
import pandas as pd
import boto3
import json

from protocol_engine import recommend as run_protocol_engine

# ---------------------------------------------------------------------------
# v1 model + endpoint (UNCHANGED) -- kept exactly as-is so existing iOS and
# Streamlit clients keep working undisturbed while /v2/recommend is validated.
# ---------------------------------------------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "neuroprana_random_forest_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"v1 model loading failed: {e}")

app = FastAPI()

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
    return {"message": "Sushumna Cloud API Running"}


@app.post("/predict")
def predict(data: dict):

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
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

        prediction = model.predict(input_df)[0]

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

        prompt = build_prompt(data, prediction, protocol)
        llm_explanation = call_bedrock(prompt)

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


# ---------------------------------------------------------------------------
# v2 model + endpoint (NEW) -- richer inputs, 3-dimension state vector with
# confidence, protocol engine as the decision layer, Bedrock explains the
# exact protocol selected. Runs alongside /predict, does not replace it yet.
# ---------------------------------------------------------------------------

STATE_MODEL_PATH = os.path.join(os.path.dirname(__file__), "sushumna_state_model_v2.pkl")

try:
    state_bundle = joblib.load(STATE_MODEL_PATH)
    state_model = state_bundle["model"]
    state_label_encoders = state_bundle["label_encoders"]
    state_feature_columns = state_bundle["feature_columns"]
    state_target_columns = state_bundle["target_columns"]
except Exception as e:
    state_bundle = None
    state_model = None
    print(f"v2 state model loading failed: {e}")


def predict_state_vector(input_dict):
    input_df = pd.DataFrame([input_dict])[state_feature_columns]
    proba_per_output = state_model.predict_proba(input_df)

    result = {}
    for i, target in enumerate(state_target_columns):
        probs = proba_per_output[i][0]
        pred_idx = probs.argmax()
        pred_label = state_label_encoders[target].inverse_transform([pred_idx])[0]
        result[target] = {
            "level": pred_label,
            "confidence": round(float(probs[pred_idx]), 2)
        }
    return result


def build_v2_prompt(state_vector, protocol):
    return f"""
A user just completed a check-in with this estimated state:

Stress: {state_vector['stress_level']['level']} (confidence {state_vector['stress_level']['confidence']})
Mood: {state_vector['mood_level']['level']} (confidence {state_vector['mood_level']['confidence']})
Clarity: {state_vector['clarity_level']['level']} (confidence {state_vector['clarity_level']['confidence']})

Based on this, they have been matched to: {protocol['technique']}
({protocol['cadence']} cadence, {protocol['rounds']} rounds, about {protocol['duration_minutes']} minutes).
Purpose of this practice: {protocol['goal']}

Generate a short, warm, non-medical explanation in 3 sentences of why this practice
fits their current check-in. Do not diagnose. Do not provide medical advice.
Do not claim certainty the state estimate doesn't support -- if any confidence
score above is below 0.5, acknowledge gently that this is an approximate read.
Keep tone calm and reassuring.
"""


@app.post("/v2/recommend")
def recommend_v2(data: dict):
    if state_model is None:
        raise HTTPException(status_code=500, detail="State model not loaded")

    try:
        model_input = {
            "mscs_score": data["mscs_score"],
            "positive_affect": data["positive_affect"],
            "negative_affect": data["negative_affect"],
            "clarity_rating": data["clarity_rating"],
            "age_band": data["age_band"],
            "practice_experience": data["practice_experience"],
            # Computed on-device from the last locally-stored check-in; the
            # very first check-in on a device won't have one yet, so the app
            # sends 0 (no known trend) rather than omitting the field.
            "previous_practice_delta": data.get("previous_practice_delta", 0.0),
        }

        state_vector = predict_state_vector(model_input)

        protocol = run_protocol_engine(
            stress_level=state_vector["stress_level"]["level"],
            mood_level=state_vector["mood_level"]["level"],
            clarity_level=state_vector["clarity_level"]["level"],
            practice_experience=data["practice_experience"],
            recent_technique_names=data.get("recent_technique_names", []),
            recent_reflections=data.get("recent_reflections", []),
        )

        prompt = build_v2_prompt(state_vector, protocol)
        llm_explanation = call_bedrock(prompt)

        if not llm_explanation:
            llm_explanation = (
                f"Based on your check-in, {protocol['technique']} is a good fit for this moment. "
                f"{protocol['goal']}"
            )

        return {
            "state_vector": state_vector,
            "protocol": protocol,
            "explanation": llm_explanation
        }

    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Missing required field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
