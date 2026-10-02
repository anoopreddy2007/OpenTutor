import uuid

from app.database.connection import SessionLocal
from app.models import (
    Attempt,
    Concept,
    Course,
    Enrollment,
    LearnerState,
    Question,
    Topic,
    User,
)
from app.services.adaptive_attempt import process_adaptive_attempt


def create_test_data(
    db,
    mastery,
    confidence,
):
    test_id = uuid.uuid4().hex

    user = User(
        username=f"adaptive_attempt_{test_id}",
        email=f"adaptive_attempt_{test_id}@example.com",
    )
    db.add(user)
    db.flush()

    course = Course(
        name=f"Adaptive Attempt Course {test_id}",
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
        name="Adaptive Attempt Topic",
    )
    db.add(topic)
    db.flush()

    concept = Concept(
        topic_id=topic.id,
        name="Adaptive Attempt Concept",
        difficulty=3,
    )
    db.add(concept)
    db.flush()

    learner_state = LearnerState(
        user_id=user.id,
        concept_id=concept.id,
        mastery=mastery,
        confidence=confidence,
        attempts_count=10,
        correct_count=int(mastery * 10),
    )
    db.add(learner_state)

    questions = [
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

    db.add_all(questions)
    db.flush()

    return user, concept, questions


def test_adaptive_attempt_updates_state_and_selects_next_question():
    db = SessionLocal()

    try:
        user, concept, questions = create_test_data(
            db=db,
            mastery=0.50,
            confidence=0.50,
        )

        attempt = Attempt(
            user_id=user.id,
            question_id=questions[0].id,
            answer="A",
            is_correct=True,
            confidence=4,
            time_taken=30,
        )

        db.add(attempt)
        db.flush()

        result = process_adaptive_attempt(
            db=db,
            attempt=attempt,
        )

        assert result.attempt.id == attempt.id

        assert result.learning_action is not None
        assert result.learning_action.concept_id == concept.id

        assert result.next_question is not None
        assert result.next_question.concept_id == concept.id

    finally:
        db.rollback()
        db.close()


def test_adaptive_attempt_with_no_available_action_returns_no_question():
    db = SessionLocal()

    try:
        test_id = uuid.uuid4().hex

        user = User(
            username=f"adaptive_no_action_{test_id}",
            email=f"adaptive_no_action_{test_id}@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name=f"No Action Course {test_id}",
        )
        db.add(course)
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="No Action Topic",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name="No Action Concept",
            difficulty=3,
        )
        db.add(concept)
        db.flush()

        question = Question(
            concept_id=concept.id,
            question_text="Question",
            question_type="multiple_choice",
            correct_answer="A",
            difficulty=3,
        )
        db.add(question)
        db.flush()

        attempt = Attempt(
            user_id=user.id,
            question_id=question.id,
            answer="A",
            is_correct=True,
            confidence=4,
        )
        db.add(attempt)
        db.flush()

        result = process_adaptive_attempt(
            db=db,
            attempt=attempt,
        )

        assert result.attempt.id == attempt.id
        assert result.learning_action.action == "NO_ACTION"
        assert result.next_question is None

    finally:
        db.rollback()
        db.close()