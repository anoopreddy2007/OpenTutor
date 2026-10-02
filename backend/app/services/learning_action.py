from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import LearnerState, RevisionState

from app.services.adaptive_policy import determine_adaptive_action
from app.services.learning_signals import (
    calculate_misconception_severity,
    calculate_revision_need,
    check_prerequisites_ready,
)
from app.services.recommendation_service import recommend_next_concept


@dataclass(frozen=True)
class LearningAction:
    action: str
    concept_id: int | None
    priority: float
    reason: str


def get_next_learning_action(
    db: Session,
    user_id: int,
    current_time: datetime | None = None,
) -> LearningAction:

    if current_time is None:
        current_time = datetime.utcnow()

    concept_id = recommend_next_concept(
        db=db,
        user_id=user_id,
    )

    if concept_id is None:
        return LearningAction(
            action="NO_ACTION",
            concept_id=None,
            priority=0.0,
            reason="No suitable learning concept is currently available.",
        )

    learner_state = (
        db.query(LearnerState)
        .filter(
            LearnerState.user_id == user_id,
            LearnerState.concept_id == concept_id,
        )
        .first()
    )

    revision_state = (
        db.query(RevisionState)
        .filter(
            RevisionState.user_id == user_id,
            RevisionState.concept_id == concept_id,
        )
        .first()
    )

    if learner_state is None:
        mastery = 0.0
        confidence = 0.0
    else:
        mastery = learner_state.mastery
        confidence = learner_state.confidence

    revision_need = calculate_revision_need(
        revision_state=revision_state,
        current_time=current_time,
    )

    misconception_severity = calculate_misconception_severity(
        learner_state=learner_state,
    )

    prerequisites_ready = check_prerequisites_ready(
        db=db,
        user_id=user_id,
        concept_id=concept_id,
    )

    decision = determine_adaptive_action(
        mastery=mastery,
        confidence=confidence,
        revision_need=revision_need,
        misconception_severity=misconception_severity,
        prerequisites_ready=prerequisites_ready,
    )

    return LearningAction(
        action=decision.action,
        concept_id=concept_id,
        priority=decision.priority,
        reason=decision.reason,
    )