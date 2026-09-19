from datetime import datetime

from sqlalchemy.orm import Session

from app.models import (
    Concept,
    ConceptPrerequisite,
    Enrollment,
    LearnerState,
    RevisionState,
    Topic,
)
from app.services.adaptive_decision import (
    calculate_adaptive_priority,
)
from app.services.recommendation_reason import (
    build_recommendation_reason,
)

PREREQUISITE_MASTERY_THRESHOLD = 0.7

MAX_DIFFICULTY = 5

REVISION_INTERVAL_DAYS = 7.0


def _is_prerequisite_ready(
    db: Session,
    user_id: int,
    concept_id: int,
) -> bool:
    prerequisites = (
        db.query(ConceptPrerequisite)
        .filter(
            ConceptPrerequisite.concept_id == concept_id
        )
        .all()
    )

    if not prerequisites:
        return True

    for prerequisite in prerequisites:
        state = (
            db.query(LearnerState)
            .filter(
                LearnerState.user_id == user_id,
                LearnerState.concept_id
                == prerequisite.prerequisite_concept_id,
            )
            .first()
        )

        if (
            state is None
            or state.mastery < PREREQUISITE_MASTERY_THRESHOLD
        ):
            return False

    return True


def _calculate_revision_need(
    revision_state: RevisionState | None,
    current_time: datetime,
    last_attempt_at: datetime | None = None,
) -> float:
    """
    Calculate revision urgency.

    RevisionState is preferred when available.

    If a concept does not yet have a RevisionState,
    fall back to the original time-based revision
    calculation using the last attempt timestamp.
    """

    if revision_state is not None:

        if revision_state.next_review_at is None:
            return 0.0

        if current_time >= revision_state.next_review_at:
            return 1.0

        if revision_state.last_review_at is None:
            return 0.0

        total_interval = (
            revision_state.next_review_at
            - revision_state.last_review_at
        ).total_seconds()

        elapsed = (
            current_time
            - revision_state.last_review_at
        ).total_seconds()

        if total_interval <= 0:
            return 1.0

        return max(
            0.0,
            min(
                1.0,
                elapsed / total_interval,
            ),
        )

    # Backward-compatible fallback for concepts
    # without a RevisionState.
    if last_attempt_at is None:
        return 0.0

    elapsed_seconds = (
        current_time - last_attempt_at
    ).total_seconds()

    elapsed_days = max(
        0.0,
        elapsed_seconds / (24 * 60 * 60),
    )

    revision_need = (
        elapsed_days / REVISION_INTERVAL_DAYS
    )

    return max(
        0.0,
        min(
            1.0,
            revision_need,
        ),
    )


def _calculate_priority(
    mastery: float,
    difficulty: float,
    last_attempt_at: datetime | None,
    current_time: datetime,
    revision_state: RevisionState | None = None,
    confidence: float = 0.0,
) -> float:
    """
    Calculate recommendation priority using the
    adaptive decision layer.

    Factors:

    1. Mastery gap
    2. Confidence gap
    3. Revision urgency
    4. Difficulty
    """

    revision_need = _calculate_revision_need(
        revision_state=revision_state,
        current_time=current_time,
        last_attempt_at=last_attempt_at,
    )

    return calculate_adaptive_priority(
        mastery=mastery,
        confidence=confidence,
        revision_need=revision_need,
        difficulty=difficulty,
        max_difficulty=MAX_DIFFICULTY,
    )


def recommend_next_concept(
    db: Session,
    user_id: int,
):
    enrolled_course_ids = (
        db.query(Enrollment.course_id)
        .filter(
            Enrollment.user_id == user_id
        )
        .all()
    )

    enrolled_course_ids = [
        course_id
        for (course_id,) in enrolled_course_ids
    ]

    if not enrolled_course_ids:
        return None

    concepts = (
        db.query(Concept)
        .join(
            Topic,
            Concept.topic_id == Topic.id,
        )
        .filter(
            Topic.course_id.in_(
                enrolled_course_ids
            )
        )
        .all()
    )

    current_time = datetime.utcnow()

    best_concept_id = None
    best_priority = -1.0

    for concept in concepts:

        if not _is_prerequisite_ready(
            db,
            user_id,
            concept.id,
        ):
            continue

        learner_state = (
            db.query(LearnerState)
            .filter(
                LearnerState.user_id == user_id,
                LearnerState.concept_id
                == concept.id,
            )
            .first()
        )

        if learner_state is None:
            mastery = 0.0
            confidence = 0.0
            last_attempt_at = None
        else:
            mastery = learner_state.mastery
            confidence = learner_state.confidence
            last_attempt_at = (
                learner_state.last_attempt_at
            )

        revision_state = (
            db.query(RevisionState)
            .filter(
                RevisionState.user_id == user_id,
                RevisionState.concept_id == concept.id,
            )
            .first()
        )

        priority = _calculate_priority(
            mastery=mastery,
            confidence=confidence,
            difficulty=concept.difficulty,
            last_attempt_at=last_attempt_at,
            current_time=current_time,
            revision_state=revision_state,
        )

        if priority > best_priority:
            best_priority = priority
            best_concept_id = concept.id

    return best_concept_id


def get_recommendation_reason(
    db: Session,
    user_id: int,
    concept_id: int,
) -> str:
    """Explain why a concept was recommended."""

    concept = db.get(Concept, concept_id)

    if concept is None:
        raise ValueError("Concept not found")

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
        last_attempt_at = None
    else:
        mastery = learner_state.mastery
        last_attempt_at = learner_state.last_attempt_at

    revision_state = (
        db.query(RevisionState)
        .filter(
            RevisionState.user_id == user_id,
            RevisionState.concept_id == concept_id,
        )
        .first()
    )

    current_time = datetime.utcnow()

    revision_need = _calculate_revision_need(
        revision_state=revision_state,
        current_time=current_time,
        last_attempt_at=last_attempt_at,
    )

    return build_recommendation_reason(
        mastery=mastery,
        revision_need=revision_need,
        difficulty=concept.difficulty,
    )