"""
Shared numeric parsing for cadence strings like "4-6" or "4-4-4-4".
Mirrors CadenceParser.swift exactly so the backend and the iOS app's local
fallback engine can never disagree about what a cadence string means.
"""
import re


def numbers(cadence: str):
    """Extract positive numbers from a cadence string, e.g. "4-8-8" -> [4.0, 8.0, 8.0]."""
    tokens = re.split(r"[^0-9.]+", cadence)
    values = []
    for t in tokens:
        if not t:
            continue
        try:
            v = float(t)
            if v > 0:
                values.append(v)
        except ValueError:
            continue
    return values


def cycle_length_seconds(cadence: str) -> float:
    """Total seconds for one full breath cycle. Falls back to a standard
    16-second box-breathing cycle (4+4+4+4) if the cadence can't be parsed."""
    values = numbers(cadence)
    return sum(values) if values else 16.0
