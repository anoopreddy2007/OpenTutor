from datetime import datetime

from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.learner_state import LearnerState
from app.models.learner_state_history import LearnerStateHistory
from app.models.question import Question
from app.models.revision_state import RevisionState
from app.services.bkt_update import update_knowledge
from app.services.revision_scheduler import schedule_next_review
from app.services.retrievability import calculate_retrievability


def _calculate_revision_stability(
    mastery: float,
) -> float:
    """
    Convert learner mastery into an initial revision stability.

    Higher mastery results in longer expected memory stability.
    """

    return max(
        1.0,
        mastery * 30.0,
    )


def update_learner_state(
    db: Session,
    attempt: Attempt,
) -> LearnerState:
    """
    Update the learner's state for the concept associated
    with the attempted question.

    Mastery is updated using Bayesian Knowledge Tracing (BKT).

    A learner-state history snapshot is recorded after each
    attempt.

    RevisionState is also updated to track forgetting,
    retrievability, stability, and the next review time.
    """

    question = db.get(
        Question,
        attempt.question_id,
    )

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

    # Update learner confidence.
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

    # Record learner-state history.
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

    # Find or create revision state.
    revision_state = (
        db.query(RevisionState)
        .filter(
            RevisionState.user_id == learner_state.user_id,
            RevisionState.concept_id == learner_state.concept_id,
        )
        .first()
    )

    if revision_state is None:
        revision_state = RevisionState(
            user_id=learner_state.user_id,
            concept_id=learner_state.concept_id,
            stability=1.0,
            difficulty=0.3,
            retrievability=1.0,
            review_count=0,
        )

        db.add(revision_state)

    # Update revision stability from current mastery.
    revision_state.stability = _calculate_revision_stability(
        learner_state.mastery
    )

    revision_state.last_review_at = attempt.created_at
    revision_state.review_count += 1

    # A review has just occurred, so retrievability resets to 1.
    revision_state.retrievability = calculate_retrievability(
        last_review_at=revision_state.last_review_at,
        current_time=revision_state.last_review_at,
        stability=revision_state.stability,
    )

    revision_state.next_review_at = schedule_next_review(
        last_review_at=revision_state.last_review_at,
        stability=revision_state.stability,
    )

    revision_state.updated_at = datetime.utcnow()

    db.flush()
    db.refresh(learner_state)

    return learner_state