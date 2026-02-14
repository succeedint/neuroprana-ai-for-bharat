
# NeuroPrana — System Design (Updated for Professional Track)

## 1) Architecture Overview
NeuroPrana follows a modular, cloud-native architecture designed for scalability, responsible AI deployment, and measurable outcome tracking.

### Primary Cloud Architecture (Hackathon Build Phase)
- **Frontend:** Streamlit UI (MVP) or AWS Amplify (future-ready)
- **API Layer:** Amazon API Gateway (REST endpoint)
- **Inference Layer:** AWS Lambda (Python-based model inference)
- **Model Hosting:**
  - Amazon SageMaker Endpoint (preferred for scalability), **or**
  - Lambda loading serialized model from Amazon S3
- **Storage:**
  - Amazon DynamoDB (anonymized session + adherence logs)
  - Amazon S3 (model artifacts, versioning, analytics exports)
- **LLM Layer:** Amazon Bedrock (Claude) for explanation generation
- **Monitoring:** Amazon CloudWatch (logs, p95 latency/error alarms; Bedrock budget guardrails)
- **Security:** IAM least-privilege access; encryption at rest (S3/DynamoDB) and in transit (TLS); optional Amazon Cognito

This architecture ensures secure, scalable, and production-aligned deployment readiness.

## 2) Data Flow
1. User completes a stress-state check-in via UI
2. API Gateway routes request to Lambda
3. Lambda preprocesses features (schema-validated)
4. ML model estimates stress-state / expected benefit class
5. Safe protocol set is filtered via guardrails
6. ML ranking selects a personalized routine
7. Bedrock generates explanation text (post-gen checks)
8. User completes the session and logs adherence
9. Session metadata stored in DynamoDB
10. Aggregated analytics optionally exported to S3

## 3) Why AI is Required
Static rule-based mappings cannot adapt to evolving stress states, learn from adherence behavior, or optimize for measurable improvement. ML enables dynamic state estimation, pattern recognition across repeated check-ins, and safe personalization; LLMs provide human-readable guidance to support adherence.

> Rules act strictly as safety guardrails and fallbacks; primary decisioning derives from ML personalization signals.

## 4) ML Design
**Learning Approach**
- Supervised learning (classification or regression)
- Synthetic dataset generated using realistic distributions inspired by public stress-scale ranges

**Feature Set**
- Stress score aggregates; positive/negative affect indicators; weekly clarity rating
- Minimal demographic band; historical adherence rate; prior session delta

**Candidate Models**
- Logistic Regression (baseline)
- Random Forest
- Gradient Boosting / XGBoost

**Evaluation Strategy**
- Train/val/test split with cross-validation
- Metrics: F1-score (classification) / RMSE (regression) + calibration assessment
- Model selection based on generalization and calibration

**Model Management**
- Serialized pipeline artifact; version tracking via S3
- Reproducible preprocessing; model card (assumptions, data type, limits, metrics)

## 5) Recommendation Logic
1. Apply safety constraints (contraindicated states filtered)
2. Use ML output to rank safe protocols
3. Select the top-ranked routine
4. Log outcome signals (adherence + post-session rating)

**Fallback:** If ML unavailable → revert to safety-rule baseline mapping.

## 6) LLM Layer
- Generates 4–6 sentence explanation (why this routine; how to practice safely; gentle motivational reinforcement)
- Explicitly avoids medical advice; includes simple safety precautions
- Tone: culturally respectful, neutral, supportive
- Post-generation validation: max length, block-list for clinical phrasing, neutrality check

**Service:** Amazon Bedrock (Claude). **Fallback:** Predefined static explanation templates.

## 7) Responsible AI & Safety
- Non-clinical preventive wellness positioning
- Prominent disclaimers and consent gating
- Clear redirection language for severe symptoms
- No diagnosis, no medical claims
- Data minimization (no PII required)
- Synthetic/public data only
- Inclusive, bias-aware language design
- Transparent “How it works & limitations” page

## 8) Deployment Strategy
**MVP (Hackathon Phase)**
- Functional working prototype with synthetic dataset
- ML inference + explanation layer
- Demonstrable AWS architecture mapping

**Production-Ready Path**
- SageMaker endpoint; API Gateway + Lambda; DynamoDB persistence; Bedrock explanations; CloudWatch monitoring

## 9) Limitations
- Synthetic dataset limits real-world generalization
- Not clinically validated; not a substitute for medical care

## 10) Future Roadmap
- Contextual bandit / reinforcement personalization
- Longitudinal outcome modeling
- Indian language localization; voice-guided interface
- Cohort dashboards for schools and workforce wellness programs
- Drift monitoring and re-training on opt-in aggregates

## 11) Observability & Ops
- CloudWatch metrics and alarms (p95 latency, error rate)
- Structured logs (no sensitive content); request IDs for tracing
- Budget guardrails for Bedrock usage
- Blue/green model version switch via environment variable

## 12) GTM Snapshot (Business Feasibility)
Initial GTM: **cohort pilots** with schools and workforce ERGs (B2B/B2B2C). Facilitator dashboards licensed to institutions; low-cost individual plan later. Partnerships with universities/NGOs/HR wellness vendors for scale.