from app.services.mastery import classify_mastery


def build_learner_summary(
    mastery: float,
    confidence: float,
    attempts_count: int,
    correct_count: int,
) -> dict:
    """Build a compact summary of the learner's current state."""
    accuracy = (
        correct_count / attempts_count
        if attempts_count > 0
        else 0.0
    )

    return {
        "mastery": mastery,
        "confidence": confidence,
        "mastery_level": classify_mastery(mastery),
        "attempts_count": attempts_count,
        "correct_count": correct_count,
        "accuracy": accuracy,
    }