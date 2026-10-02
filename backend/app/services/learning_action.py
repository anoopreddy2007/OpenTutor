from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models import LearnerState
from app.services.adaptive_policy import determine_adaptive_action
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
) -> LearningAction:
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

    if learner_state is None:
        mastery = 0.0
        confidence = 0.0
    else:
        mastery = learner_state.mastery
        confidence = learner_state.confidence

    decision = determine_adaptive_action(
        mastery=mastery,
        confidence=confidence,
        revision_need=0.0,
        misconception_severity=0.0,
        prerequisites_ready=True,
    )

    return LearningAction(
        action=decision.action,
        concept_id=concept_id,
        priority=decision.priority,
        reason=decision.reason,
    )