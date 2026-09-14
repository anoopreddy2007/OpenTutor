from app.services.learner_model import clamp


def adjust_mastery_by_confidence(
    mastery: float,
    confidence: float,
) -> float:
    """Adjust mastery slightly using learner confidence."""

    mastery = clamp(mastery)
    confidence = clamp(confidence)

    adjustment = 0.05 * (confidence - 0.5)

    return clamp(mastery + adjustment)