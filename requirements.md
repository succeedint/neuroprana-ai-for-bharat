
# NeuroPrana — Requirements (Updated for Professional Track)

## 1. Overview
NeuroPrana is an AI-powered preventive stress-state modeling and adaptive breath-based intervention support system designed to improve emotional regulation outcomes through safe, non-clinical guidance. It leverages validated stress and affect frameworks (PSS/PANAS-inspired measures), supervised machine learning for personalization, and LLM-generated explanations — with clear non-clinical guardrails and responsible AI design. NeuroPrana supports preventive self-regulation using validated measures; it does not measure neural change or provide medical advice.

## 2. Problem Statement
High stress and emotional dysregulation are widespread across students, professionals, and communities. While breath-based practices are evidence-informed and culturally rooted, most digital wellness tools provide generic, static content that does not adapt to a user’s evolving state.

**Need:**
- Personalized, adaptive non-clinical support
- Measurable progress tracking
- Responsible AI guidance with clear safety boundaries
- Scalable systems suitable for school and workforce contexts

## 3. Why AI is Necessary (Not Rule-Based)
Static rules cannot adapt to individual patterns over time. ML enables pattern detection across repeated check-ins, supports measurable outcome modeling, and allows evidence-based personalization at scale. LLMs provide concise, personalized explanations that can strengthen clarity and adherence.

> Rules are used only as safety guardrails and fallbacks — primary decisioning derives from ML personalization signals.

## 4. Target Users & Beneficiaries
- Students and educators (readiness to learn, emotional regulation)
- Working professionals (burnout prevention and day-to-day regulation)
- Schools, universities, and community wellness programs
- Workforce wellness initiatives and organizational pilots

Primary context: scalable preventive emotional support in India and similar ecosystems.

## 5. Goals & Success Criteria
**Primary Goals**
- Provide fast, personalized state check-ins
- Recommend adaptive breath-based routines
- Improve adherence and self-regulation over time
- Offer transparent, safety-aware explanations

**Targets (pilot intent)**
- ≥70% weekly check-ins by week 4
- ≥60% session adherence by weeks 2–4
- ≥10–15% improvement from baseline on short PSS/PANAS-inspired measures by week 8–12

## 6. Scope (MVP)
**In Scope**
- Short self-report state check-in (weekly + optional daily micro-check)
- ML-driven protocol selection; rules only for safety constraints
- LLM-generated explanation (non-clinical)
- Basic progress trend visualization
- Explicit disclaimers and consent gating
- Synthetic/public dataset only
- Anonymized session logging; no PII

**Out of Scope**
- Clinical diagnosis or medical claims
- Emergency triage or crisis handling
- Physiological sensors or medical devices
- Storage of personally identifiable information

## 7. Functional Requirements
- FR-1: Capture weekly stress-state check-in (scores + timestamp)
- FR-2: Recommend a pranayama protocol using a trained ML model (classifier/regressor) with safety constraints applied post-selection
- FR-3: Generate a concise, safety-aware explanation and motivation message via LLM
- FR-4: Capture adherence and quick post-session self-rating
- FR-5: Display trends vs baseline (simple deltas and adherence)
- FR-6: Require consent acknowledgement before use
- FR-7: Provide aggregated, anonymized metrics export for cohort pilots (optional)

## 8. Non-Functional Requirements
- NFR-1: Privacy-first; no PII required
- NFR-2: Model training uses synthetic/public data only
- NFR-3: Graceful fallback to rule-only safety mode if ML/LLM unavailable
- NFR-4: Recommendation latency under 2 seconds (demo conditions)
- NFR-5: Mobile-friendly, clear language UI
- NFR-6: Logging for performance and error monitoring (no sensitive content)
- NFR-7: Localization-ready for Indian languages (future phase)
- NFR-8: Schema validation for all API payloads
- NFR-9: CloudWatch alarms on p95 latency/error; Bedrock budget guardrails

## 9. Data & Labels (Hackathon Phase)
**Synthetic dataset** generated using realistic distributions inspired by publicly available ranges of PSS/PANAS-style measures. Simulated records include:
- Repeated user check-ins (anonymized `anon_id`)
- Stress and affect scores; weekly clarity
- Minimal demographic band (e.g., age group)
- Adherence patterns; pre/post session ratings

**Labels**
- Stress-state bucket (Low / Moderate / High)
- Predicted benefit class
- Adherence classification
- Improvement delta from baseline

All training and evaluation during the hackathon phase will use synthetic or publicly available data only, in compliance with challenge guidelines.

## 10. AI / ML Requirements
- ML-1: Train a supervised model to estimate stress-state or expected benefit class from check-in features
- ML-2: Use model output to rank/select among predefined pranayama protocols
- ML-3: Log adherence + post-session rating to enable future reinforcement learning loop
- ML-4: Provide plain-language explanation of recommendation rationale (model card)
- ML-5: No medical prediction tasks
- ML-6: Maintain a model card per version (data type, assumptions, limitations, metrics)

**Candidate baseline models:** Logistic Regression (baseline), Random Forest, Gradient Boosting / XGBoost

## 11. LLM Requirements
- LLM-1: Generate 4–6 sentence explanation (why this routine, safe practice guidance, gentle motivation)
- LLM-2: Avoid medical advice; include simple safety guidance (e.g., stop if dizzy)
- LLM-3: Tone must be culturally respectful and non-judgmental
- LLM-4: Post-generation checks: max length, block list for medical phrasing, neutral tone verification

Planned service: **AWS Bedrock (Claude)**; cached fallbacks if unavailable.

## 12. Responsible AI & Safety
- Non-clinical preventive wellness support only
- Prominent disclaimers; consent-first design
- Clear redirection language for severe symptoms
- Inclusive, neutral language
- Data minimization; anonymized storage
- Transparent “How it works & limitations” section in-app

## 13. Proposed AWS Architecture (Build Phase)
**Frontend:** Streamlit UI (MVP) or AWS Amplify

**API Layer:** API Gateway + AWS Lambda (Python)

**Model Hosting:** SageMaker endpoint (preferred) **or** Lambda loading serialized model from S3

**LLM:** AWS Bedrock (Claude)

**Data Storage:** DynamoDB (session logs), S3 (artifacts, aggregated analytics)

**Monitoring:** CloudWatch logs & metrics; p95 latency/error alarms; Bedrock budget guardrails

**Security:** IAM least-privilege roles; encryption at rest (S3/DynamoDB) and in transit (TLS); optional Cognito for basic auth/consent

## 14. Assumptions & Constraints
- Hackathon requires meaningful AI beyond rule-based systems
- Only synthetic/public data permitted
- AWS services must be clearly integrated in the build phase
- Time-boxed MVP prioritizes clarity and demonstrability

## 15. Risks & Mitigations
- LLM downtime → cached explanations; rule-only mode
- Over-claim risk → non-clinical copy; model cards; “How it works” page
- Data realism (synthetic) → disclosed; plan opt-in aggregate pilots
- Latency spikes → CloudWatch alarms; small models; pre-warm strategy

## 16. Roadmap (Post-MVP)
- Personalization upgrade: contextual bandit / reinforcement loop
- Cohort dashboards for schools and workforce programs
- Indian language localization; voice guidance
- Longitudinal outcome modeling
- Drift monitoring and re-training on opt-in aggregates

## 17. Hackathon Deliverables
- GitHub repository containing: `requirements.md`, `design.md`
- Presentation deck (PDF)
- Model card (appendix)

## 17. Hackathon Deliverables (Idea Submission Phase)
- GitHub repository containing:
  - `requirements.md`
  - `design.md`
- Presentation deck (PDF format)

(Note: Working prototype, video pitch, and AWS deployment artifacts are part of later phases if shortlisted.)