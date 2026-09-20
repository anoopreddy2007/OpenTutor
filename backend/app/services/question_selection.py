from app.models.question import Question


def calculate_question_priority(
    question: Question,
    mastery: float,
    confidence: float,
) -> float:
    """
    Calculate how suitable a question is for the learner.

    The priority considers:

    - mastery gap
    - confidence gap
    - difficulty suitability

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

    # Estimate whether the learner is ready for the
    # difficulty level of the question.
    readiness_gap = max(
        0.0,
        normalized_difficulty - mastery,
    )

    difficulty_fit = 1.0 - readiness_gap

    priority = (
        0.45 * mastery_gap
        + 0.25 * confidence_gap
        + 0.30 * difficulty_fit
    )

    return max(
        0.0,
        min(1.0, priority),
    )


def select_next_question(
    questions: list[Question],
    mastery: float,
    confidence: float,
) -> Question | None:
    """
    Select the most suitable question for the learner.
    """

    if not questions:
        return None

    best_question = None
    best_priority = -1.0

    for question in questions:
        priority = calculate_question_priority(
            question=question,
            mastery=mastery,
            confidence=confidence,
        )

        if priority > best_priority:
            best_priority = priority
            best_question = question

    return best_question