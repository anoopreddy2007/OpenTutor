import uuid

from app.database.connection import SessionLocal
from app.models import (
    Concept,
    ConceptPrerequisite,
    Course,
    Enrollment,
    LearnerState,
    Topic,
    User,
)
from app.services.recommendation_service import recommend_next_concept


def test_recommends_concept_when_no_prerequisites():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"recommend_user_{test_id}",
            email=f"recommend_user_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"Recommendation Course {test_id}",
        )
        db.add(course)
        db.flush()

        # Enroll the user in the course
        db.add(
            Enrollment(
                user_id=user.id,
                course_id=course.id,
            )
        )
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="Recommendation Topic",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name="Basic Concept",
            difficulty=2,
        )
        db.add(concept)
        db.flush()

        recommended = recommend_next_concept(
            db,
            user.id,
        )

        assert recommended == concept.id

    finally:
        db.rollback()
        db.close()


def test_unmet_prerequisite_blocks_recommendation():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"prereq_user_{test_id}",
            email=f"prereq_user_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"Prerequisite Course {test_id}",
        )
        db.add(course)
        db.flush()

        # Enroll the user in the course
        db.add(
            Enrollment(
                user_id=user.id,
                course_id=course.id,
            )
        )
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="Prerequisite Topic",
        )
        db.add(topic)
        db.flush()

        prerequisite = Concept(
            topic_id=topic.id,
            name="Prerequisite Concept",
            difficulty=2,
        )

        advanced = Concept(
            topic_id=topic.id,
            name="Advanced Concept",
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
        db.flush()

        recommended = recommend_next_concept(
            db,
            user.id,
        )

        # The advanced concept is blocked because
        # its prerequisite has not been mastered.
        assert recommended == prerequisite.id

    finally:
        db.rollback()
        db.close()


def test_mastery_affects_recommendation_priority():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"mastery_user_{test_id}",
            email=f"mastery_user_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"Mastery Course {test_id}",
        )
        db.add(course)
        db.flush()

        # Enroll the user in the course
        db.add(
            Enrollment(
                user_id=user.id,
                course_id=course.id,
            )
        )
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="Mastery Topic",
        )
        db.add(topic)
        db.flush()

        weak_concept = Concept(
            topic_id=topic.id,
            name="Weak Concept",
            difficulty=2,
        )

        strong_concept = Concept(
            topic_id=topic.id,
            name="Strong Concept",
            difficulty=2,
        )

        db.add_all([
            weak_concept,
            strong_concept,
        ])
        db.flush()

        db.add_all([
            LearnerState(
                user_id=user.id,
                concept_id=weak_concept.id,
                mastery=0.2,
                confidence=0.5,
                attempts_count=5,
                correct_count=1,
            ),
            LearnerState(
                user_id=user.id,
                concept_id=strong_concept.id,
                mastery=0.9,
                confidence=0.9,
                attempts_count=10,
                correct_count=9,
            ),
        ])
        db.flush()

        recommended = recommend_next_concept(
            db,
            user.id,
        )

        # The weak concept has a larger mastery gap,
        # so it should have the higher priority.
        assert recommended == weak_concept.id

    finally:
        db.rollback()
        db.close()