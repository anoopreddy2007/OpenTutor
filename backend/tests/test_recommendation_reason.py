import uuid

from app.database.connection import SessionLocal
from app.models import (
    Concept,
    Course,
    Enrollment,
    Topic,
    User,
)
from app.services.recommendation_reason import (
    build_recommendation_reason,
)
from app.services.recommendation_service import (
    get_recommendation_reason,
)
def test_low_mastery_produces_reason():
    reason = build_recommendation_reason(
        mastery=0.2,
        revision_need=0.0,
        difficulty=2,
    )

    assert "significant practice" in reason


def test_revision_due_produces_reason():
    reason = build_recommendation_reason(
        mastery=0.8,
        revision_need=1.0,
        difficulty=2,
    )

    assert "due for revision" in reason


def test_developing_mastery_produces_reason():
    reason = build_recommendation_reason(
        mastery=0.5,
        revision_need=0.0,
        difficulty=2,
    )

    assert "additional practice" in reason


def test_difficult_concept_produces_reason():
    reason = build_recommendation_reason(
        mastery=0.8,
        revision_need=0.0,
        difficulty=5,
    )

    assert "challenging concept" in reason


def test_default_reason_exists():
    reason = build_recommendation_reason(
        mastery=0.8,
        revision_need=0.0,
        difficulty=2,
    )

    assert reason == (
        "Recommended as the next suitable concept "
        "for your learning."
    )
def test_recommendation_reason_for_new_concept():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"reason_user_{test_id}",
            email=f"reason_user_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"Reason Course {test_id}",
        )
        db.add(course)
        db.flush()

        db.add(
            Enrollment(
                user_id=user.id,
                course_id=course.id,
            )
        )
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="Reason Topic",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name="New Concept",
            difficulty=2,
        )
        db.add(concept)
        db.flush()

        reason = get_recommendation_reason(
            db,
            user.id,
            concept.id,
        )

        assert "significant practice" in reason

    finally:
        db.rollback()
        db.close()    