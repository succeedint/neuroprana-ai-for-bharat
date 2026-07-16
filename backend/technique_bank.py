"""
Server-side technique bank -- mirrors TechniqueBank.swift exactly (same
names, cadences, tag ranges, rounds options, and gating) so the iOS local
engine and this backend engine produce comparable output while both are
validated side by side. Adds intensity/instructions/safety_note, which the
Swift version doesn't need since HowToPracticeView already has its own
generic on-screen steps.

Cadence (the breath ratio itself) and practice-level gating are treated as
fixed, vetted values -- these are the physiologically load-bearing
parameters, so they are not algorithmically varied. Rounds and Reflection
are the freely-variable layers on top.
"""

GENERIC_SAFETY = (
    "Stop if you feel dizzy, lightheaded, or uncomfortable, and return to "
    "natural breathing. This is general wellness guidance, not medical advice."
)

RETENTION_SAFETY = (
    GENERIC_SAFETY
    + " Breath retention is not recommended during pregnancy or with "
    "uncontrolled high blood pressure -- check with a healthcare provider first."
)

VIGOROUS_SAFETY = (
    GENERIC_SAFETY
    + " This is a brisk, activating practice -- avoid it during pregnancy, "
    "with hypertension, or if rapid breathing tends to make you lightheaded."
)

TECHNIQUE_BANK = [
    {
        "name": "Anulom Vilom — Simple (Alternate Nostril)",
        "cadence": "4-4",
        "goal": "A gentle, balancing breath suited to almost any moment — a good starting point.",
        "stress_range": (0, 4),
        "mood_range": (0, 4),
        "clarity_range": (0, 4),
        "min_practice_level": None,
        "rounds_options": [6, 8, 10, 12],
        "reflection_category": "balancing",
        "intensity": "gentle",
        "instructions": (
            "Sit comfortably with your spine upright. Close your right nostril "
            "with your thumb and inhale through the left. Close the left nostril "
            "and exhale through the right. Inhale right, then exhale left. That's one round."
        ),
        "safety_note": GENERIC_SAFETY,
    },
    {
        "name": "Anulom Vilom — Deepening (with gentle retention)",
        "cadence": "4-8-8",
        "goal": "Adds a brief hold to deepen the balancing effect as your practice grows.",
        "stress_range": (2, 4),
        "mood_range": (0, 3),
        "clarity_range": (0, 4),
        "min_practice_level": 0.34,
        "rounds_options": [4, 6, 8],
        "reflection_category": "balancing",
        "intensity": "moderate",
        "instructions": (
            "Same alternate-nostril pattern as the simple version, with a gentle "
            "hold at the top of each inhale before exhaling. Keep the hold soft, never strained."
        ),
        "safety_note": RETENTION_SAFETY,
    },
    {
        "name": "Anulom Vilom — Extended (long retention)",
        "cadence": "8-16-16",
        "goal": "A slower, deeper practice for steady, experienced practitioners seeking profound calm.",
        "stress_range": (3, 4),
        "mood_range": (0, 2),
        "clarity_range": (0, 4),
        "min_practice_level": 0.67,
        "rounds_options": [3, 4, 5],
        "reflection_category": "calming",
        "intensity": "advanced",
        "instructions": (
            "Alternate-nostril breathing with an extended hold. Only attempt the full "
            "hold length if it stays comfortable -- shorten it any time you need to."
        ),
        "safety_note": RETENTION_SAFETY,
    },
    {
        "name": "Bhramari (Humming Bee Breath)",
        "cadence": "4-8",
        "goal": "The gentle vibration and long exhale help soothe an agitated nervous system.",
        "stress_range": (3, 4),
        "mood_range": (0, 4),
        "clarity_range": (0, 4),
        "min_practice_level": None,
        "rounds_options": [5, 7, 9],
        "reflection_category": "calming",
        "intensity": "gentle",
        "instructions": (
            "Close your eyes, inhale gently, and as you exhale make a soft, steady "
            "humming sound, like a bee. Keep your jaw relaxed throughout."
        ),
        "safety_note": GENERIC_SAFETY,
    },
    {
        "name": "Sheetali (Cooling Breath)",
        "cadence": "4-6",
        "goal": "A cooling breath to ease an overheated, agitated state of mind.",
        "stress_range": (3, 4),
        "mood_range": (0, 1),
        "clarity_range": (0, 4),
        "min_practice_level": None,
        "rounds_options": [5, 7, 9],
        "reflection_category": "calming",
        "intensity": "gentle",
        "instructions": (
            "Curl your tongue lengthwise (or purse your lips if you can't curl your "
            "tongue) and inhale slowly through it, then exhale gently through the nose."
        ),
        "safety_note": GENERIC_SAFETY,
    },
    {
        "name": "Extended Exhale Calming Breath",
        "cadence": "4-7-8",
        "goal": "A longer exhale than inhale to quickly settle an overwhelmed nervous system.",
        "stress_range": (4, 4),
        "mood_range": (0, 0),
        "clarity_range": (0, 4),
        "min_practice_level": None,
        "rounds_options": [4, 6, 8],
        "reflection_category": "calming",
        "intensity": "moderate",
        "instructions": (
            "Inhale quietly through the nose, hold gently, then exhale slowly and "
            "completely through the mouth, making a soft whoosh sound."
        ),
        "safety_note": RETENTION_SAFETY,
    },
    {
        "name": "Ujjayi (Ocean Breath)",
        "cadence": "4-4",
        "goal": "A slow, audible breath that builds steady focus and presence.",
        "stress_range": (1, 3),
        "mood_range": (1, 4),
        "clarity_range": (0, 2),
        "min_practice_level": None,
        "rounds_options": [6, 8, 10],
        "reflection_category": "focusing",
        "intensity": "moderate",
        "instructions": (
            "Breathe through the nose while slightly constricting the back of your "
            "throat, creating a soft ocean-like sound on both the inhale and exhale."
        ),
        "safety_note": GENERIC_SAFETY,
    },
    {
        "name": "Balanced Breath (Box Breathing)",
        "cadence": "4-4-4-4",
        "goal": "An even, structured rhythm to stabilize emotional state and improve clarity.",
        "stress_range": (1, 3),
        "mood_range": (1, 3),
        "clarity_range": (1, 3),
        "min_practice_level": None,
        "rounds_options": [4, 6, 8],
        "reflection_category": "balancing",
        "intensity": "gentle",
        "instructions": (
            "Inhale for a count of four, hold for four, exhale for four, hold for "
            "four. Keep each phase even and unforced."
        ),
        "safety_note": GENERIC_SAFETY,
    },
    {
        "name": "Bhastrika-Inspired Energizing Breath",
        "cadence": "2-2",
        "goal": "A brisk, equal rhythm to build alertness and positive activation.",
        "stress_range": (0, 1),
        "mood_range": (0, 1),
        "clarity_range": (0, 1),
        "min_practice_level": None,
        "rounds_options": [10, 15, 20],
        "reflection_category": "energizing",
        "intensity": "vigorous",
        "instructions": (
            "Breathe in and out through the nose at an even, brisk pace, keeping "
            "each breath equal in length. Slow down immediately if you feel lightheaded."
        ),
        "safety_note": VIGOROUS_SAFETY,
    },
    {
        "name": "Surya Bhedana-Inspired Warming Breath",
        "cadence": "3-2",
        "goal": "A quicker inhale emphasis to build energy and heat when feeling low.",
        "stress_range": (0, 1),
        "mood_range": (0, 2),
        "clarity_range": (0, 2),
        "min_practice_level": None,
        "rounds_options": [8, 10, 12],
        "reflection_category": "energizing",
        "intensity": "moderate",
        "instructions": (
            "Inhale through the right nostril only (closing the left with a "
            "finger), then exhale through the nose normally. Repeat at a steady pace."
        ),
        "safety_note": GENERIC_SAFETY,
    },
]
