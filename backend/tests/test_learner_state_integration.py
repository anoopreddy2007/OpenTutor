from app.database.connection import SessionLocal
from app.models import Attempt, Concept, Question, Topic, Course, User
from app.services.learner_state_service import update_learner_state


def test_learner_state_created_after_attempt():
    db = SessionLocal()

    try:
        user = User(
            username="test_learner",
            email="test_learner@example.com",
        )
        db.add(user)
        db.flush()

        course = Course(
            name="Test Course",
            description="Course used for testing",
        )
        db.add(course)
        db.flush()

        topic = Topic(
            course_id=course.id,
            name="Test Topic",
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name="Test Concept",
            difficulty=2,
        )
        db.add(concept)
        db.flush()

        question = Question(
            concept_id=concept.id,
            question_text="What is testing?",
            question_type="multiple_choice",
            difficulty=2,
            correct_answer="A",
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

        learner_state = update_learner_state(db, attempt)

        assert learner_state.user_id == user.id
        assert learner_state.concept_id == concept.id
        assert learner_state.attempts_count == 1
        assert learner_state.correct_count == 1
        assert learner_state.mastery > 0.0
        assert learner_state.confidence > 0.0

    finally:
        db.rollback()
        db.close()