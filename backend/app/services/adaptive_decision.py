from app.services.learner_model import clamp, mastery_gap


def calculate_adaptive_priority(
    mastery: float,
    confidence: float,
    revision_need: float,
    difficulty: float,
    max_difficulty: float = 5.0,
) -> float:
    """
    Calculate adaptive learning priority.

    Higher priority means the learner has a stronger reason
    to work on the concept next.
    """

    mastery_gap_value = mastery_gap(mastery)

    confidence_gap = clamp(
        1.0 - confidence,
    )

    revision_need = clamp(revision_need)

    if max_difficulty <= 0:
        raise ValueError("max_difficulty must be greater than 0")

    difficulty_fit = clamp(
        difficulty / max_difficulty,
    )

    priority = (
        0.40 * mastery_gap_value
        + 0.20 * confidence_gap
        + 0.30 * revision_need
        + 0.10 * difficulty_fit
    )

    return clamp(priority)