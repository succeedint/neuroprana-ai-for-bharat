import streamlit as st
import requests

API_URL = "https://b6pcmtrbsh.us-east-1.awsapprunner.com/predict"

st.set_page_config(
    page_title="NeuroPrana",
    page_icon="🧠",
    layout="centered"
)

# --- Branding Header ---
st.markdown(
    """
    <h1 style='text-align: center;'>🧠 NeuroPrana</h1>
    <h4 style='text-align: center; color: gray;'>
    AI-Powered Preventive Stress-State Modeling
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("""
NeuroPrana models your current stress and emotional state 
and recommends a personalized breath-based protocol 
for safe, preventive self-regulation support.
""")

# --- Input Section ---

st.markdown("### 🌿 Stress & Emotional Assessment")

st.markdown(
"There are no right or wrong answers. Use your best sense of how you’ve been feeling recently."
)

# -------------------------------
# 🧘 Emotional State Check In
# -------------------------------
with st.expander("🧘 Emotional State Check In", expanded=True):

    stress_score = st.slider(
        "Stress Score (PSS-style) (0–40)",
        0, 40, 20,
        help="Higher score indicates higher perceived stress over the past week."
    )

    clarity_rating = st.slider(
        "Clarity Rating (1–10)",
        1, 10, 5,
        help="How mentally clear and focused do you feel right now?"
    )

# -------------------------------
# 🌱 Emotional Balance
# -------------------------------
with st.expander("🌱 Emotional Balance"):

    col1, col2 = st.columns(2)

    with col1:
        positive_affect = st.slider(
            "Positive Affect (0–50)",
            0, 50, 25,
            help="How strongly are you feeling positive emotions (joy, calm, optimism)?"
        )

    with col2:
        negative_affect = st.slider(
            "Negative Affect (0–50)",
            0, 50, 25,
            help="How strongly are you feeling stress, anxiety, or frustration?"
        )

# -------------------------------
# 📅 Practice History
# -------------------------------
with st.expander("📅 Practice History"):

    col3, col4 = st.columns(2)

    with col3:
        recent_days = st.slider(
            "Recent Practice (Last 7 Days)",
            0, 7, 3,
            help="How many days in the last 7 did you practice breathwork?"
        )
        adherence_rate = recent_days / 7

    with col4:
        prior_days = st.slider(
            "Prior Practice (Last 30 Days)",
            0, 30, 10,
            help="How many days in the last 30 did you practice?"
        )
        prior_adherence = prior_days / 30

# -------------------------------
# 🌤 Baseline Comparison & Age
# -------------------------------
with st.expander("🌤 Personal Context"):

    baseline_change = st.select_slider(
        "Compared to your usual state, today feels:",
        options=["Much Worse", "Worse", "Same", "Better", "Much Better"],
        value="Same"
    )

    baseline_map = {
        "Much Worse": -5,
        "Worse": -2,
        "Same": 0,
        "Better": 2,
        "Much Better": 5
    }

    prior_delta = baseline_map[baseline_change]

    age_band = st.selectbox(
        "Age Band",
        ["18-25", "26-40", "41-60"],
        help="Used to personalize modeling based on age group."
    )
st.markdown("")

if st.button("✨ Generate Recommendation"):

    payload = {
        "stress_score": stress_score,
        "positive_affect": positive_affect,
        "negative_affect": negative_affect,
        "clarity_rating": clarity_rating,
        "adherence_rate": adherence_rate,
        "prior_delta": prior_delta,
        "age_band": age_band,
        "prior_adherence": prior_adherence
    }

    with st.spinner("Analyzing your state and generating protocol..."):

        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()
                prediction = result["predicted_stress_state"]
                protocol = result["recommended_protocol"]

                st.markdown("---")
                st.markdown("## 🧠 Model Output")

                # --- Stress Level Indicator ---
                if prediction == "High":
                    st.error(f"🔴 Predicted Stress State: {prediction}")
                elif prediction == "Moderate":
                    st.warning(f"🟡 Predicted Stress State: {prediction}")
                else:
                    st.success(f"🟢 Predicted Stress State: {prediction}")

                st.markdown("### 🌿 Recommended Breath Protocol")

                st.markdown(f"""
                **Protocol:** {protocol['protocol_name']}  
                **Duration:** {protocol['duration_minutes']} minutes  
                **Cadence:** {protocol['cadence']}  
                **Goal:** {protocol['goal']}
                """)

                st.markdown("### ✨ Model Interpretation")
                st.info(result["explanation"])

                # Progress bar
                stress_progress = 0.8 if prediction=="High" else 0.5 if prediction=="Moderate" else 0.2
                st.progress(stress_progress)

                st.markdown("### 🫁 How to Practice")

                st.markdown(
                    "Sit comfortably with your spine upright. "
                    "Breathe gently through the nose. "
                    "If at any point you feel dizzy or uncomfortable, "
                    "stop and return to normal breathing."
                )              

                st.markdown("---")

            else:
                st.error(f"API Error: {response.status_code}")

        except Exception as e:
            st.error(f"Connection error: {e}")

            st.markdown("---")

st.markdown(
    "<p style='font-size:12px; color:gray;'>"
    "NeuroPrana is a preventive AI-based stress-state modeling system. "
    "This tool is for educational and self-regulation support purposes only "
    "and is not a medical diagnostic instrument."
    "</p>",
    unsafe_allow_html=True
)