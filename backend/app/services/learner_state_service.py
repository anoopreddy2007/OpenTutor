from datetime import datetime

from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.learner_state import LearnerState
from app.models.question import Question


def update_learner_state(
    db: Session,
    attempt: Attempt,
) -> LearnerState:
    """
    Update the learner's state for the concept associated
    with the attempted question.
    """

    question = db.get(Question, attempt.question_id)

    if question is None:
        raise ValueError("Question not found")

    learner_state = (
        db.query(LearnerState)
        .filter(
            LearnerState.user_id == attempt.user_id,
            LearnerState.concept_id == question.concept_id,
        )
        .first()
    )

    if learner_state is None:
        learner_state = LearnerState(
            user_id=attempt.user_id,
            concept_id=question.concept_id,
            mastery=0.0,
            confidence=0.0,
            attempts_count=0,
            correct_count=0,
        )
        db.add(learner_state)

    learner_state.attempts_count += 1

    if attempt.is_correct:
        learner_state.correct_count += 1

    # Difficulty-aware mastery update.
    learning_rate = 0.10 + (question.difficulty - 1) * 0.025

    if attempt.is_correct:
        learner_state.mastery += learning_rate * (
            1.0 - learner_state.mastery
        )
    else:
        learner_state.mastery -= learning_rate * learner_state.mastery

    learner_state.mastery = max(
        0.0,
        min(1.0, learner_state.mastery),
    )

    if attempt.confidence is not None:
        confidence = attempt.confidence / 5.0

        learner_state.confidence += 0.20 * (
            confidence - learner_state.confidence
        )

        learner_state.confidence = max(
            0.0,
            min(1.0, learner_state.confidence),
        )

    learner_state.last_attempt_at = attempt.created_at
    learner_state.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(learner_state)

    return learner_state