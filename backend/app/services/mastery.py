def classify_mastery(mastery: float) -> str:
    """Classify a learner based on their mastery score."""
    mastery = max(0.0, min(1.0, mastery))

    if mastery < 0.30:
        return "beginner"

    if mastery < 0.70:
        return "developing"

    return "proficient"