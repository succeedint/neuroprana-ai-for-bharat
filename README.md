🧠 NeuroPrana

AI-Powered Preventive Stress-State Modeling for Bharat

⸻

## Track
AI for Healthcare & Life Sciences (Professional Track)

⸻

🌿 Problem Statement

India faces a growing mental wellness challenge — particularly among youth and working professionals.

Most digital wellness tools today are:
	•	Reactive instead of preventive
	•	Chatbot-based without structured modeling
	•	Emotionally supportive but not physiologically grounded
	•	Lacking deterministic stress-state assessment

There is a need for a safe, structured, AI-assisted preventive system that helps users understand their stress state and receive grounded self-regulation guidance.

⸻

🧠 Solution Overview

NeuroPrana is a hybrid AI system that combines:
	•	Classical Machine Learning for deterministic stress-state classification
	•	Generative AI (Amazon Bedrock – Claude Sonnet 4.6) for supportive, human-readable explanations
	•	Structured breath protocol recommendations

The system provides:
	•	Real-time stress prediction
	•	Personalized non-medical explanation
	•	Actionable breath-based guidance
	•	Preventive emotional regulation support

⸻

⚙️ Why Generative AI is Required

The ML model produces a classification label (Low / Moderate / High).

However, users need:
	•	Context
	•	Emotional reassurance
	•	Clear guidance
	•	Calm tone

Amazon Bedrock (Claude Sonnet 4.6) is used to:
	•	Translate structured ML output into supportive language
	•	Maintain non-clinical tone
	•	Avoid medical diagnosis
	•	Improve user trust and clarity

The LLM does not control prediction logic.
It only generates explanation based on deterministic ML output.

⸻

☁️ AWS Services Used
	•	Amazon Bedrock – Claude Sonnet 4.6 (explanation layer)
	•	AWS App Runner – Containerized backend hosting
	•	Amazon ECR – Docker image registry
	•	FastAPI (Dockerized) – API layer
	•	Streamlit Cloud – Frontend hosting

⸻

🔄 System Architecture

User Inputs
↓
FastAPI API (App Runner)
↓
Random Forest Classifier (Scikit-learn)
↓
Breath Protocol Selection
↓
Amazon Bedrock (Claude Sonnet 4.6)
↓
Personalized Explanation
↓
Streamlit UI Display

⸻

🛡 Safety & Design Principles
	•	Deterministic ML core
	•	LLM restricted to explanation only
	•	No PII storage
	•	No medical advice
	•	Guardrails in prompt design
	•	Preventive framing

This layered approach ensures reliability, safety, and explainability.

⸻

🚀 Live Prototype

🔗 https://neuroprana-ai-for-bharat.streamlit.app/

⸻

🌏 Impact for Bharat

NeuroPrana is designed for:
	•	Mobile-first digital populations
	•	Preventive daily emotional regulation
	•	Youth and early-career professionals
	•	Scalable AI-enabled wellness

By combining structured ML with safe generative explanation, NeuroPrana bridges technical AI innovation with culturally relevant mental wellness delivery.

⸻

🔮 Future Roadmap
	•	Native mobile deployment (iOS & Android)
	•	Multilingual support (Hindi + regional languages)
	•	Tone personalization
	•	Guided breath session timer
	•	Privacy-preserving stress insights
	•	Edge-ready deployment for low-bandwidth environments

⸻

🏆 Innovation Highlights
	•	Hybrid ML + LLM layered architecture
	•	Secure Amazon Bedrock integration
	•	Cloud-native containerized deployment
	•	Separation of classification and explanation layers
	•	Preventive mental wellness positioning

⸻

👥 Team

Succeed International LLC
AI + Wellness Integration Initiative
