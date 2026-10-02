from app.models.question import Question


def calculate_question_priority(
    question: Question,
    mastery: float,
    confidence: float,
    action: str = "PRACTICE_CONCEPT",
) -> float:
    """
    Calculate how suitable a question is for the learner.

    The priority considers:

    - mastery gap
    - confidence gap
    - difficulty suitability
    - adaptive learning action

    Higher difficulty is increasingly penalized when the
    learner has not demonstrated sufficient mastery.
    """

    mastery = max(
        0.0,
        min(1.0, mastery),
    )

    confidence = max(
        0.0,
        min(1.0, confidence),
    )

    question_difficulty = max(
        1,
        min(5, question.difficulty),
    )

    mastery_gap = 1.0 - mastery
    confidence_gap = 1.0 - confidence

    normalized_difficulty = (
        question_difficulty / 5.0
    )

    readiness_gap = max(
        0.0,
        normalized_difficulty - mastery,
    )

    difficulty_fit = 1.0 - readiness_gap

    # Preserve the original adaptive scoring.
    # This is used for normal practice.
    base_priority = (
        0.45 * mastery_gap
        + 0.25 * confidence_gap
        + 0.30 * difficulty_fit
    )

    # Prerequisites should be handled before
    # selecting a question from the current concept.
    if action == "REVIEW_PREREQUISITES":
        return 0.0

    # Remediation and confidence building favor
    # easier questions.
    if action in {
        "REMEDIATE_MISCONCEPTION",
        "BUILD_CONFIDENCE",
    }:
        action_adjustment = (
            1.0 - normalized_difficulty
        )

    # Advancement favors harder questions.
    elif action == "ADVANCE":
        action_adjustment = normalized_difficulty

    # Revision favors questions appropriate for
    # the learner's demonstrated ability.
    elif action == "REVIEW_CONCEPT":
        action_adjustment = difficulty_fit

    # Normal practice retains the original
    # adaptive difficulty behavior.
    elif action == "PRACTICE_CONCEPT":
        return max(
            0.0,
            min(1.0, base_priority),
        )

    # Unknown actions safely fall back to
    # difficulty suitability.
    else:
        action_adjustment = difficulty_fit

    priority = (
        0.70 * base_priority
        + 0.30 * action_adjustment
    )

    return max(
        0.0,
        min(1.0, priority),
    )


def select_next_question(
    questions: list[Question],
    mastery: float,
    confidence: float,
    action: str = "PRACTICE_CONCEPT",
) -> Question | None:
    """
    Select the most suitable question for the learner
    based on the current adaptive learning action.
    """

    if not questions:
        return None

    if action == "REVIEW_PREREQUISITES":
        return None

    best_question = None
    best_priority = -1.0

    for question in questions:
        priority = calculate_question_priority(
            question=question,
            mastery=mastery,
            confidence=confidence,
            action=action,
        )

        if priority > best_priority:
            best_priority = priority
            best_question = question

    return best_question