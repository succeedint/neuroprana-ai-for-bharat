
import pandas as pd
import joblib

# Load model
model = joblib.load("models/neuroprana_random_forest_model.pkl")

protocol_library = {
    "High": {
        "protocol_name": "Calming Breath (Slow Diaphragmatic)",
        "duration_minutes": 5,
        "cadence": "4-6 breathing (4 sec inhale, 6 sec exhale)",
        "goal": "Reduce sympathetic activation and calm stress response"
    },
    "Moderate": {
        "protocol_name": "Balanced Breath (Box Breathing)",
        "duration_minutes": 4,
        "cadence": "4-4-4-4 (inhale-hold-exhale-hold)",
        "goal": "Stabilize emotional state and improve clarity"
    },
    "Low": {
        "protocol_name": "Energizing Breath (Bellows Style - Gentle)",
        "duration_minutes": 3,
        "cadence": "Moderate rhythmic breathing",
        "goal": "Increase alertness and positive activation"
    }
}

def generate_explanation(stress_state, protocol):
    return f"""
Based on your recent check-in, your current emotional state is categorized as {stress_state}.

We recommend the {protocol['protocol_name']} for approximately {protocol['duration_minutes']} minutes.

This breathing pattern ({protocol['cadence']}) is intended to help you {protocol['goal']}.

Please practice gently. Stop if you feel dizzy or uncomfortable.
This is preventive wellness guidance and not medical advice.
""".strip()


def neuroprana_inference(input_dict):
    input_df = pd.DataFrame([input_dict])
    predicted_state = model.predict(input_df)[0]
    protocol = protocol_library[predicted_state]
    explanation = generate_explanation(predicted_state, protocol)

    return {
        "predicted_stress_state": predicted_state,
        "recommended_protocol": protocol,
        "explanation": explanation
    }
