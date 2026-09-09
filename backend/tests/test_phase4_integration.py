import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_complete_learning_flow():
    # Generate unique test data so repeated test runs do not collide
    test_id = uuid.uuid4().hex[:8]

    username = f"integration_student_{test_id}"
    email = f"integration_student_{test_id}@example.com"
    course_name = f"Integration Test Course {test_id}"
    topic_name = f"Python Basics {test_id}"
    concept_name = f"Variables {test_id}"

    # 1. Create user
    user_response = client.post(
        "/users/",
        json={
            "username": username,
            "email": email,
        },
    )

    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    # 2. Create course
    course_response = client.post(
        "/courses/",
        json={
            "name": course_name,
            "description": "Course for Phase 4 integration testing",
        },
    )

    assert course_response.status_code == 201
    course_id = course_response.json()["id"]

    # 3. Enroll user
    from app.database.connection import SessionLocal
    from app.models.enrollment import Enrollment

    db = SessionLocal()

    try:
        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
        )
        db.add(enrollment)
        db.commit()
    finally:
        db.close()

    # 4. Create topic
    topic_response = client.post(
        "/topics/",
        json={
            "course_id": course_id,
            "name": topic_name,
            "description": "Basic Python concepts",
            "order_index": 1,
        },
    )

    assert topic_response.status_code == 201
    topic_id = topic_response.json()["id"]

    # 5. Create concept
    concept_response = client.post(
        "/concepts/",
        json={
            "topic_id": topic_id,
            "name": concept_name,
            "description": "Python variables",
            "difficulty": 1,
        },
    )

    assert concept_response.status_code == 201
    concept_id = concept_response.json()["id"]

    # 6. Create question
    question_response = client.post(
        "/questions/",
        json={
            "concept_id": concept_id,
            "question_text": "Which keyword is used to define a variable in Python?",
            "question_type": "multiple_choice",
            "difficulty": 1,
            "options": {
                "A": "var",
                "B": "let",
                "C": "No keyword is required",
                "D": "define",
            },
            "correct_answer": "C",
            "explanation": "Python variables are created through assignment.",
        },
    )

    assert question_response.status_code == 201
    question_id = question_response.json()["id"]

    # 7. Submit attempt
    attempt_response = client.post(
        "/attempts/",
        json={
            "user_id": user_id,
            "question_id": question_id,
            "answer": "C",
            "is_correct": True,
            "time_taken": 10.5,
            "confidence": 4,
        },
    )

    assert attempt_response.status_code == 201

    # 8. Verify learner state
    state_response = client.get(
        f"/learner-states/user/{user_id}/concept/{concept_id}"
    )

    assert state_response.status_code == 200

    state = state_response.json()

    assert state["user_id"] == user_id
    assert state["concept_id"] == concept_id
    assert state["attempts_count"] == 1
    assert state["correct_count"] == 1
    assert state["mastery"] > 0
    assert state["confidence"] > 0

    # 9. Get recommendation
    recommendation_response = client.get(
        f"/recommendations/next/{user_id}"
    )

    assert recommendation_response.status_code == 200

    recommendation = recommendation_response.json()

    assert "concept_id" in recommendation
    assert recommendation["concept_id"] is not None