"""
Shared level indexing for the three intake dimensions, mirroring
DimensionLevel + IntakeProfile in the iOS app (0 = lowest, 4 = highest).
The state model returns level names as strings (e.g. "High"); this module
converts those to/from the 0-4 integer scale the protocol engine's
distance-based matching uses, exactly like the Swift TechniqueEngine does.
"""

STRESS_LABELS = ["Very Low", "Low", "Moderate", "High", "Very High"]
CLARITY_LABELS = ["Very Low", "Low", "Moderate", "High", "Very High"]
MOOD_LABELS = ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]


def index_for_label(label: str, labels: list) -> int:
    try:
        return labels.index(label)
    except ValueError:
        # Unexpected label from the model -- fail safe to the middle tier
        # rather than crashing the recommendation flow.
        return 2
