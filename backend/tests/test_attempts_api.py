from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_attempt_endpoint():
    response = client.post(
        "/attempts/",
        json={
            "user_id": 1,
            "question_id": 1,
            "answer": "A",
            "is_correct": True,
            "time_taken": 20.0,
            "confidence": 4,
        },
    )

    assert response.status_code in {201, 404}