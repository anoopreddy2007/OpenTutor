from datetime import datetime

from app.database.connection import SessionLocal
from app.models import (
    Concept,
    ConceptPrerequisite,
    Course,
    LearnerState,
    RevisionState,
    Topic,
    User,
)
from app.services.learning_signals import (
    calculate_misconception_severity,
    calculate_revision_need,
    check_prerequisites_ready,
)


def test_revision_need_is_inverse_of_retrievability():
    revision_state = RevisionState(
        user_id=1,
        concept_id=1,
        stability=5.0,
        difficulty=0.3,
        retrievability=0.25,
    )

    revision_need = calculate_revision_need(
        revision_state=revision_state,
        current_time=datetime(2026, 1, 1),
    )

    assert revision_need == 0.75


def test_missing_revision_state_has_no_revision_need():
    revision_need = calculate_revision_need(
        revision_state=None,
        current_time=datetime(2026, 1, 1),
    )

    assert revision_need == 0.0


def test_misconception_severity_increases_with_errors():
    learner_state = LearnerState(
        user_id=1,
        concept_id=1,
        mastery=0.20,
        confidence=0.30,
        attempts_count=10,
        correct_count=2,
    )

    severity = calculate_misconception_severity(
        learner_state,
    )

    assert severity > 0.70


def test_new_learner_has_no_misconception_signal():
    learner_state = LearnerState(
        user_id=1,
        concept_id=1,
        mastery=0.0,
        confidence=0.0,
        attempts_count=0,
        correct_count=0,
    )

    severity = calculate_misconception_severity(
        learner_state,
    )

    assert severity == 0.0


def test_concept_without_prerequisites_is_ready():
    db = SessionLocal()

    try:
        user = User(
            username="signal_test_user",
            email="signal_test@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name="Signal Test Course",
        )
        db.add(course)
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="Signal Topic",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name="Independent Concept",
            difficulty=2,
        )
        db.add(concept)
        db.flush()

        assert check_prerequisites_ready(
            db=db,
            user_id=user.id,
            concept_id=concept.id,
        ) is True

    finally:
        db.rollback()
        db.close()


def test_prerequisite_requires_sufficient_mastery():
    db = SessionLocal()

    try:
        user = User(
            username="prereq_signal_user",
            email="prereq_signal@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name="Prerequisite Signal Course",
        )
        db.add(course)
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="Prerequisite Topic",
        )
        db.add(topic)
        db.flush()

        prerequisite = Concept(
            topic_id=topic.id,
            name="Prerequisite",
            difficulty=2,
        )

        advanced = Concept(
            topic_id=topic.id,
            name="Advanced",
            difficulty=4,
        )

        db.add_all([
            prerequisite,
            advanced,
        ])
        db.flush()

        db.add(
            ConceptPrerequisite(
                concept_id=advanced.id,
                prerequisite_concept_id=prerequisite.id,
            )
        )

        db.add(
            LearnerState(
                user_id=user.id,
                concept_id=prerequisite.id,
                mastery=0.50,
                confidence=0.50,
                attempts_count=5,
                correct_count=2,
            )
        )

        db.flush()

        assert check_prerequisites_ready(
            db=db,
            user_id=user.id,
            concept_id=advanced.id,
        ) is False

    finally:
        db.rollback()
        db.close()