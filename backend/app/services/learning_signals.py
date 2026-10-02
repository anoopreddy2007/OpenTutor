from datetime import datetime

from sqlalchemy.orm import Session

from app.models import ConceptPrerequisite, LearnerState, RevisionState


PREREQUISITE_MASTERY_THRESHOLD = 0.70


def calculate_revision_need(
    revision_state: RevisionState | None,
    current_time: datetime,
) -> float:
    if revision_state is None:
        return 0.0

    retrievability = max(
        0.0,
        min(1.0, revision_state.retrievability),
    )

    return max(
        0.0,
        min(1.0, 1.0 - retrievability),
    )


def check_prerequisites_ready(
    db: Session,
    user_id: int,
    concept_id: int,
) -> bool:
    prerequisites = (
        db.query(ConceptPrerequisite)
        .filter(
            ConceptPrerequisite.concept_id == concept_id,
        )
        .all()
    )

    if not prerequisites:
        return True

    prerequisite_ids = [
        prerequisite.prerequisite_concept_id
        for prerequisite in prerequisites
    ]

    learner_states = (
        db.query(LearnerState)
        .filter(
            LearnerState.user_id == user_id,
            LearnerState.concept_id.in_(prerequisite_ids),
        )
        .all()
    )

    mastery_by_concept = {
        state.concept_id: state.mastery
        for state in learner_states
    }

    return all(
        mastery_by_concept.get(prerequisite_id, 0.0)
        >= PREREQUISITE_MASTERY_THRESHOLD
        for prerequisite_id in prerequisite_ids
    )


def calculate_misconception_severity(
    learner_state: LearnerState | None,
) -> float:
    if learner_state is None:
        return 0.0

    attempts = learner_state.attempts_count

    if attempts <= 0:
        return 0.0

    accuracy = (
        learner_state.correct_count / attempts
    )

    mastery_gap = max(
        0.0,
        min(1.0, 1.0 - learner_state.mastery),
    )

    error_rate = max(
        0.0,
        min(1.0, 1.0 - accuracy),
    )

    misconception_severity = (
        0.60 * error_rate
        + 0.40 * mastery_gap
    )

    return max(
        0.0,
        min(1.0, misconception_severity),
    )