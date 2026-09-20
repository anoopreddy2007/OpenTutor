import uuid

from app.database.connection import SessionLocal
from app.models import (
    Concept,
    Course,
    Enrollment,
    LearnerState,
    Question,
    Topic,
    User,
)
from app.services.adaptive_learning import (
    select_next_learning_question,
)


def test_returns_none_when_no_concept_is_recommended():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"adaptive_none_{test_id}",
            email=f"adaptive_none_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        result = select_next_learning_question(
            db=db,
            user_id=user.id,
        )

        assert result is None

    finally:
        db.rollback()
        db.close()


def test_returns_question_for_recommended_concept():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"adaptive_user_{test_id}",
            email=f"adaptive_user_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"Adaptive Course {test_id}",
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
            name=f"Adaptive Topic {test_id}",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name=f"Adaptive Concept {test_id}",
            difficulty=2,
        )
        db.add(concept)
        db.flush()

        question = Question(
            concept_id=concept.id,
            question_text="What is a variable?",
            question_type="multiple_choice",
            difficulty=2,
            correct_answer="A named storage location",
        )
        db.add(question)
        db.flush()

        result = select_next_learning_question(
            db=db,
            user_id=user.id,
        )

        assert result is not None
        assert result.id == question.id

    finally:
        db.rollback()
        db.close()


def test_returns_none_when_recommended_concept_has_no_questions():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"adaptive_empty_{test_id}",
            email=f"adaptive_empty_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"Empty Question Course {test_id}",
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
            name=f"Empty Question Topic {test_id}",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name=f"Empty Question Concept {test_id}",
            difficulty=2,
        )
        db.add(concept)
        db.flush()

        result = select_next_learning_question(
            db=db,
            user_id=user.id,
        )

        assert result is None

    finally:
        db.rollback()
        db.close()


def test_question_selection_uses_learner_state():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"adaptive_state_{test_id}",
            email=f"adaptive_state_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"State Course {test_id}",
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
            name=f"State Topic {test_id}",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name=f"State Concept {test_id}",
            difficulty=2,
        )
        db.add(concept)
        db.flush()

        easy_question = Question(
            concept_id=concept.id,
            question_text="Easy question",
            question_type="multiple_choice",
            difficulty=1,
            correct_answer="A",
        )

        hard_question = Question(
            concept_id=concept.id,
            question_text="Hard question",
            question_type="multiple_choice",
            difficulty=5,
            correct_answer="B",
        )

        db.add_all(
            [
                easy_question,
                hard_question,
            ]
        )
        db.flush()

        db.add(
            LearnerState(
                user_id=user.id,
                concept_id=concept.id,
                mastery=0.2,
                confidence=0.8,
                attempts_count=5,
                correct_count=1,
            )
        )
        db.flush()

        result = select_next_learning_question(
            db=db,
            user_id=user.id,
        )

        assert result is not None
        assert result.id == easy_question.id

    finally:
        db.rollback()
        db.close()