"""
Server-side protocol engine -- mirrors TechniqueEngine.swift. Picks a
technique against the model's state vector, respects practice-level
gating, avoids recent repeats (history supplied by the client, since this
backend is stateless and there are no accounts), and layers Rounds +
Reflection on top of the vetted technique/cadence choice.
"""
import random

from technique_bank import TECHNIQUE_BANK
from reflection_bank import prompts_for
from cadence_parser import cycle_length_seconds
from dimension_levels import STRESS_LABELS, MOOD_LABELS, CLARITY_LABELS, index_for_label


def _distance(value: int, range_tuple) -> int:
    low, high = range_tuple
    if low <= value <= high:
        return 0
    return (low - value) if value < low else (value - high)


def _pick_technique(stress_idx, mood_idx, clarity_idx, practice_experience, recent_technique_names):
    eligible = [
        t for t in TECHNIQUE_BANK
        if t["min_practice_level"] is None or practice_experience >= t["min_practice_level"]
    ]

    def score(t):
        return (
            _distance(stress_idx, t["stress_range"])
            + _distance(mood_idx, t["mood_range"])
            + _distance(clarity_idx, t["clarity_range"])
        )

    not_recent = [t for t in eligible if t["name"] not in recent_technique_names]
    pool = not_recent if not_recent else eligible

    ranked = sorted(pool, key=score)
    best_score = score(ranked[0]) if ranked else 0
    top_matches = [t for t in ranked if score(t) == best_score]

    return random.choice(top_matches) if top_matches else (ranked[0] if ranked else TECHNIQUE_BANK[0])


def _pick_reflection(category, recent_reflections):
    prompts = prompts_for(category)
    not_recent = [p for p in prompts if p not in recent_reflections]
    pool = not_recent if not_recent else prompts
    return random.choice(pool)


def recommend(
    stress_level: str,
    mood_level: str,
    clarity_level: str,
    practice_experience: float,
    recent_technique_names=None,
    recent_reflections=None,
):
    """
    Takes the state vector's level labels (as returned by the trained model)
    and picks a full protocol. Returns a dict ready to serialize as the API
    response's "protocol" field.
    """
    recent_technique_names = recent_technique_names or []
    recent_reflections = recent_reflections or []

    stress_idx = index_for_label(stress_level, STRESS_LABELS)
    mood_idx = index_for_label(mood_level, MOOD_LABELS)
    clarity_idx = index_for_label(clarity_level, CLARITY_LABELS)

    technique = _pick_technique(stress_idx, mood_idx, clarity_idx, practice_experience, recent_technique_names)

    rounds = random.choice(technique["rounds_options"])
    cycle_seconds = cycle_length_seconds(technique["cadence"])
    duration_minutes = max(1, int((rounds * cycle_seconds / 60) + 0.999))  # ceil

    reflection = _pick_reflection(technique["reflection_category"], recent_reflections)

    reason = (
        f"Matched to {stress_level.lower()} stress, {mood_level.lower()} mood, "
        f"and {clarity_level.lower()} clarity."
    )

    return {
        "technique": technique["name"],
        "cadence": technique["cadence"],
        "rounds": rounds,
        "duration_minutes": duration_minutes,
        "intensity": technique["intensity"],
        "instructions": technique["instructions"],
        "reason": reason,
        "safety_guidance": technique["safety_note"],
        "goal": technique["goal"],
        "reflection": reflection,
    }
