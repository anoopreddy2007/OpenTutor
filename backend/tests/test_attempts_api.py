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

    if response.status_code == 201:
        data = response.json()

        assert "attempt_id" in data
        assert "action" in data
        assert "priority" in data
        assert "reason" in data
        assert "mastery" in data
        assert "confidence" in data
        assert "revision_need" in data
        assert "misconception_severity" in data
        assert "prerequisites_ready" in data
        assert "next_question_id" in data