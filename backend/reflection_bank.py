"""
Closing reflection prompts, mirroring ReflectionBank.swift. Purely textual
variety -- no physiological parameter here, so this can carry as many
variants as we want without any safety review.
"""

REFLECTIONS = {
    "calming": [
        "Notice how your shoulders feel now compared to when you started.",
        "Let this settled feeling stay with you for the next few minutes.",
        "Notice the space between your thoughts, even if just for a moment.",
        "There's no need to rush back — let this calm linger a little longer.",
    ],
    "energizing": [
        "Notice where you feel more awake in your body right now.",
        "Carry this alertness into whatever you turn to next.",
        "Notice any lightness or brightness in how you're feeling.",
        "Let this fresh energy set the tone for the next little while.",
    ],
    "balancing": [
        "Notice how steady and even your breath feels right now.",
        "This balance is available to you again whenever you need it.",
        "Notice if your thoughts feel a little more settled than before.",
        "Carry this sense of steadiness into your next task.",
    ],
    "focusing": [
        "Notice how clear your next thought feels.",
        "This is a good moment to gently return to what needs your attention.",
        "Notice if your mind feels a little quieter now.",
        "Let this clarity guide what you choose to focus on next.",
    ],
}


def prompts_for(category: str):
    return REFLECTIONS.get(category, REFLECTIONS["balancing"])
