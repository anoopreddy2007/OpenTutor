from datetime import datetime

from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.learner_state import LearnerState
from app.models.learner_state_history import LearnerStateHistory
from app.models.question import Question
from app.services.bkt_update import update_knowledge


def update_learner_state(
    db: Session,
    attempt: Attempt,
) -> LearnerState:
    """
    Update the learner's state for the concept associated
    with the attempted question.

    Mastery is updated using Bayesian Knowledge Tracing (BKT).
    A historical snapshot of the learner state is recorded
    after every attempt.
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

    # Bayesian Knowledge Tracing mastery update.
    learner_state.mastery = update_knowledge(
        knowledge=learner_state.mastery,
        is_correct=attempt.is_correct,
    )

    # Update learner confidence from the self-reported score.
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

    db.flush()

    # Record a snapshot of the learner's state after this attempt.
    history = LearnerStateHistory(
        user_id=learner_state.user_id,
        concept_id=learner_state.concept_id,
        mastery=learner_state.mastery,
        confidence=learner_state.confidence,
        attempts_count=learner_state.attempts_count,
        correct_count=learner_state.correct_count,
        recorded_at=learner_state.updated_at,
    )

    db.add(history)
    db.flush()

    db.refresh(learner_state)

    return learner_state