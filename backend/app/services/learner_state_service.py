from datetime import datetime

from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.learner_state import LearnerState
from app.models.learner_state_history import LearnerStateHistory
from app.models.question import Question
from app.models.revision_state import RevisionState
from app.services.bkt_update import update_knowledge
from app.services.fsrs import (
    FSRSState,
    initialize_fsrs_state,
    update_fsrs_state,
)
from app.services.fsrs_scheduler import (
    schedule_next_fsrs_review,
)


def update_learner_state(
    db: Session,
    attempt: Attempt,
) -> LearnerState:
    """
    Update the learner's state for the concept associated
    with the attempted question.

    The learner state is updated using:

    - Bayesian Knowledge Tracing (BKT) for mastery
    - confidence from the learner's attempt
    - FSRS-style memory state for revision

    A learner-state history snapshot is recorded after
    each attempt.

    RevisionState stores:

    - stability
    - difficulty
    - retrievability
    - last review time
    - next review time
    - review count
    """

    question = db.get(
        Question,
        attempt.question_id,
    )

    if question is None:
        raise ValueError("Question not found")

    # ---------------------------------------------------------
    # Learner state
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Bayesian Knowledge Tracing
    # ---------------------------------------------------------

    learner_state.mastery = update_knowledge(
        knowledge=learner_state.mastery,
        is_correct=attempt.is_correct,
    )

    # ---------------------------------------------------------
    # Confidence update
    # ---------------------------------------------------------

    if attempt.confidence is not None:
        confidence = attempt.confidence / 5.0

        learner_state.confidence += 0.20 * (
            confidence - learner_state.confidence
        )

        learner_state.confidence = max(
            0.0,
            min(
                1.0,
                learner_state.confidence,
            ),
        )

    learner_state.last_attempt_at = attempt.created_at
    learner_state.updated_at = datetime.utcnow()

    db.flush()

    # ---------------------------------------------------------
    # Learner-state history
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Revision / FSRS state
    # ---------------------------------------------------------

    revision_state = (
        db.query(RevisionState)
        .filter(
            RevisionState.user_id == learner_state.user_id,
            RevisionState.concept_id == learner_state.concept_id,
        )
        .first()
    )

    if revision_state is None:
        initial_fsrs_state = initialize_fsrs_state()

        revision_state = RevisionState(
            user_id=learner_state.user_id,
            concept_id=learner_state.concept_id,
            stability=initial_fsrs_state.stability,
            difficulty=initial_fsrs_state.difficulty,
            retrievability=initial_fsrs_state.retrievability,
            review_count=0,
        )

        db.add(revision_state)
        db.flush()

    # ---------------------------------------------------------
    # Calculate elapsed time since previous review
    # ---------------------------------------------------------

    elapsed_days = 0.0

    if revision_state.last_review_at is not None:
        elapsed_seconds = (
            attempt.created_at
            - revision_state.last_review_at
        ).total_seconds()

        elapsed_days = max(
            0.0,
            elapsed_seconds / (24 * 60 * 60),
        )

    # ---------------------------------------------------------
    # Convert database state into FSRS state
    # ---------------------------------------------------------

    fsrs_state = FSRSState(
        stability=revision_state.stability,
        difficulty=revision_state.difficulty,
        retrievability=revision_state.retrievability,
    )

    # ---------------------------------------------------------
    # Convert attempt outcome into review rating
    #
    # Correct answer    -> Good (3)
    # Incorrect answer  -> Again (1)
    # ---------------------------------------------------------

    rating = 3 if attempt.is_correct else 1

    updated_fsrs_state = update_fsrs_state(
        state=fsrs_state,
        rating=rating,
        elapsed_days=elapsed_days,
    )

    # ---------------------------------------------------------
    # Persist updated FSRS state
    # ---------------------------------------------------------

    revision_state.stability = (
        updated_fsrs_state.stability
    )

    revision_state.difficulty = (
        updated_fsrs_state.difficulty
    )

    revision_state.retrievability = (
        updated_fsrs_state.retrievability
    )

    revision_state.last_review_at = attempt.created_at
    revision_state.review_count += 1

    revision_state.next_review_at = (
        schedule_next_fsrs_review(
            last_review_at=revision_state.last_review_at,
            stability=revision_state.stability,
        )
    )

    revision_state.updated_at = datetime.utcnow()

    db.flush()

    db.refresh(learner_state)

    return learner_state