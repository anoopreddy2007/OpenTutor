def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 1.0,
) -> float:
    """Keep a learner-state value within its valid range."""
    return max(minimum, min(maximum, value))


def mastery_gap(mastery: float) -> float:
    """Return how far the learner is from complete mastery."""
    return clamp(1.0 - mastery)


def normalize_confidence(confidence: int | None) -> float:
    """Convert a 1-5 confidence score into a 0-1 value."""
    if confidence is None:
        return 0.0

    return clamp(confidence / 5.0)