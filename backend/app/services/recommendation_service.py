from datetime import datetime

from sqlalchemy.orm import Session

from app.models import (
    Concept,
    ConceptPrerequisite,
    Enrollment,
    LearnerState,
    Topic,
)


PREREQUISITE_MASTERY_THRESHOLD = 0.7

MASTERY_GAP_WEIGHT = 0.50
REVISION_WEIGHT = 0.30
DIFFICULTY_WEIGHT = 0.20

MAX_DIFFICULTY = 5
REVISION_INTERVAL_DAYS = 7


def _is_prerequisite_ready(
    db: Session,
    user_id: int,
    concept_id: int,
) -> bool:
    """
    Check whether all prerequisites for a concept
    have reached the required mastery threshold.
    """

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
    last_attempt_at: datetime | None,
    current_time: datetime,
) -> float:
    """
    Calculate how urgently a concept needs revision.

    Concepts that have not been attempted recently receive
    a higher revision score.

    The score ranges from 0.0 to 1.0.

    No previous attempt means no revision need because the
    concept is treated as new learning rather than revision.
    """

    if last_attempt_at is None:
        return 0.0

    elapsed_seconds = (
        current_time - last_attempt_at
    ).total_seconds()

    elapsed_days = elapsed_seconds / (24 * 60 * 60)

    revision_need = (
        elapsed_days / REVISION_INTERVAL_DAYS
    )

    return max(
        0.0,
        min(1.0, revision_need),
    )


def _calculate_priority(
    mastery: float,
    difficulty: int,
    last_attempt_at: datetime | None,
    current_time: datetime,
) -> float:
    """
    Calculate the recommendation priority for a concept.

    Higher priority means the learner should study
    the concept sooner.

    Priority is based on:

    - Mastery gap
    - Revision need
    - Difficulty fit
    """

    mastery_gap = 1.0 - mastery

    revision_need = _calculate_revision_need(
        last_attempt_at=last_attempt_at,
        current_time=current_time,
    )

    difficulty_fit = difficulty / MAX_DIFFICULTY

    priority = (
        MASTERY_GAP_WEIGHT * mastery_gap
        + REVISION_WEIGHT * revision_need
        + DIFFICULTY_WEIGHT * difficulty_fit
    )

    return priority


def recommend_next_concept(
    db: Session,
    user_id: int,
) -> int | None:
    """
    Recommend the next concept for a learner.

    Only concepts belonging to courses in which the
    learner is enrolled are considered.

    Concepts whose prerequisites are not sufficiently
    mastered are excluded.

    The remaining concept with the highest priority
    is returned.
    """

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
            Topic.course_id.in_(enrolled_course_ids)
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
                LearnerState.concept_id == concept.id,
            )
            .first()
        )

        if learner_state is None:
            mastery = 0.0
            last_attempt_at = None
        else:
            mastery = learner_state.mastery
            last_attempt_at = learner_state.last_attempt_at

        priority = _calculate_priority(
            mastery=mastery,
            difficulty=concept.difficulty,
            last_attempt_at=last_attempt_at,
            current_time=current_time,
        )

        if priority > best_priority:
            best_priority = priority
            best_concept_id = concept.id

    return best_concept_id