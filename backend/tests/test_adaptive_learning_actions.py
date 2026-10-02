from app.models import (
    Concept,
    Course,
    Enrollment,
    LearnerState,
    Question,
    Topic,
    User,
)
from app.database.connection import SessionLocal
from app.services.adaptive_learning import select_next_learning_question


def create_test_data(
    db,
    username,
    email,
    mastery,
    confidence,
):
    user = User(
        username=username,
        email=email,
    )
    db.add(user)
    db.flush()

    course = Course(
        name=f"{username} Course",
    )
    db.add(course)
    db.flush()

    enrollment = Enrollment(
        user_id=user.id,
        course_id=course.id,
    )
    db.add(enrollment)
    db.flush()

    topic = Topic(
        course_id=course.id,
        name=f"{username} Topic",
    )
    db.add(topic)
    db.flush()

    concept = Concept(
        topic_id=topic.id,
        name=f"{username} Concept",
        difficulty=3,
    )
    db.add(concept)
    db.flush()

    db.add(
        LearnerState(
            user_id=user.id,
            concept_id=concept.id,
            mastery=mastery,
            confidence=confidence,
            attempts_count=10,
            correct_count=int(mastery * 10),
        )
    )

    db.add_all(
        [
            Question(
                concept_id=concept.id,
                question_text="Easy question",
                question_type="multiple_choice",
                correct_answer="A",
                difficulty=1,
            ),
            Question(
                concept_id=concept.id,
                question_text="Medium question",
                question_type="multiple_choice",
                correct_answer="B",
                difficulty=3,
            ),
            Question(
                concept_id=concept.id,
                question_text="Hard question",
                question_type="multiple_choice",
                correct_answer="C",
                difficulty=5,
            ),
        ]
    )

    db.flush()

    return user, concept


def test_adaptive_learning_selects_question_for_low_mastery():
    db = SessionLocal()

    try:
        user, concept = create_test_data(
            db=db,
            username="adaptive_low_mastery",
            email="adaptive_low_mastery@example.com",
            mastery=0.20,
            confidence=0.80,
        )

        selected = select_next_learning_question(
            db=db,
            user_id=user.id,
        )

        assert selected is not None
        assert selected.concept_id == concept.id

    finally:
        db.rollback()
        db.close()


def test_adaptive_learning_selects_easier_question_for_low_confidence():
    db = SessionLocal()

    try:
        user, concept = create_test_data(
            db=db,
            username="adaptive_confidence",
            email="adaptive_confidence@example.com",
            mastery=0.50,
            confidence=0.10,
        )

        selected = select_next_learning_question(
            db=db,
            user_id=user.id,
        )

        assert selected is not None
        assert selected.concept_id == concept.id
        assert selected.difficulty == 1

    finally:
        db.rollback()
        db.close()


def test_adaptive_learning_returns_none_when_no_concept_available():
    db = SessionLocal()

    try:
        user = User(
            username="adaptive_no_concept",
            email="adaptive_no_concept@example.com",
        )

        db.add(user)
        db.flush()

        selected = select_next_learning_question(
            db=db,
            user_id=user.id,
        )

        assert selected is None

    finally:
        db.rollback()
        db.close()