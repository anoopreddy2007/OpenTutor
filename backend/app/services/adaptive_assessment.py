from dataclasses import dataclass


@dataclass(frozen=True)
class AdaptiveAssessmentDecision:
    """
    Decision about the difficulty of the next question.
    """

    target_difficulty: float
    mastery_gap: float
    confidence_gap: float
    difficulty_adjustment: float


def calculate_target_difficulty(
    mastery: float,
    confidence: float,
    current_difficulty: float,
    min_difficulty: float = 1.0,
    max_difficulty: float = 5.0,
) -> AdaptiveAssessmentDecision:
    """
    Determine the target difficulty for the next question.

    The decision considers:

    - learner mastery
    - learner confidence
    - current question difficulty

    Lower mastery/confidence moves the target toward
    easier questions.

    Higher mastery/confidence allows the target to
    move toward more difficult questions.
    """

    if min_difficulty >= max_difficulty:
        raise ValueError(
            "min_difficulty must be less than max_difficulty"
        )

    mastery = max(0.0, min(1.0, mastery))
    confidence = max(0.0, min(1.0, confidence))

    current_difficulty = max(
        min_difficulty,
        min(max_difficulty, float(current_difficulty)),
    )

    mastery_gap = 1.0 - mastery
    confidence_gap = 1.0 - confidence

    readiness = (
        0.60 * mastery
        + 0.40 * confidence
    )

    if readiness >= 0.80:
        difficulty_adjustment = 0.50

    elif readiness >= 0.60:
        difficulty_adjustment = 0.25

    elif readiness <= 0.30:
        difficulty_adjustment = -0.50

    elif readiness <= 0.45:
        difficulty_adjustment = -0.25

    else:
        difficulty_adjustment = 0.0

    target_difficulty = max(
        min_difficulty,
        min(
            max_difficulty,
            current_difficulty + difficulty_adjustment,
        ),
    )

    return AdaptiveAssessmentDecision(
        target_difficulty=target_difficulty,
        mastery_gap=mastery_gap,
        confidence_gap=confidence_gap,
        difficulty_adjustment=difficulty_adjustment,
    )