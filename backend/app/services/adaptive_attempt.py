from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models import Attempt, Question
from app.services.adaptive_learning import select_next_learning_question
from app.services.learning_action import (
    LearningAction,
    get_next_learning_action,
)
from app.services.learner_state_service import update_learner_state


@dataclass(frozen=True)
class AdaptiveAttemptResult:
    attempt: Attempt
    learning_action: LearningAction
    next_question: Question | None


def process_adaptive_attempt(
    db: Session,
    attempt: Attempt,
) -> AdaptiveAttemptResult:
    """
    Process a learner attempt through the complete adaptive loop.

    Flow:

        Attempt
            ↓
        Update learner state
            ↓
        Determine next learning action
            ↓
        Select next question

    The attempt itself is assumed to already exist in the
    current database transaction.
    """

    update_learner_state(
        db=db,
        attempt=attempt,
    )

    learning_action = get_next_learning_action(
        db=db,
        user_id=attempt.user_id,
    )

    if learning_action.action == "NO_ACTION":
        return AdaptiveAttemptResult(
            attempt=attempt,
            learning_action=learning_action,
            next_question=None,
        )

    next_question = select_next_learning_question(
        db=db,
        user_id=attempt.user_id,
    )

    return AdaptiveAttemptResult(
        attempt=attempt,
        learning_action=learning_action,
        next_question=next_question,
    )