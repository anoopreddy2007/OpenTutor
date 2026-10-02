from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_learning_action_returns_valid_response():
    response = client.get("/learning-actions/100")

    assert response.status_code == 200

    data = response.json()

    assert "action" in data
    assert "concept_id" in data
    assert "priority" in data
    assert "reason" in data
    assert "mastery" in data
    assert "confidence" in data
    assert "revision_need" in data
    assert "misconception_severity" in data
    assert "prerequisites_ready" in data


def test_get_learning_action_has_correct_data_types():
    response = client.get("/learning-actions/100")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["action"], str)
    assert data["concept_id"] is None or isinstance(data["concept_id"], int)
    assert isinstance(data["priority"], (int, float))
    assert isinstance(data["reason"], str)
    assert isinstance(data["mastery"], (int, float))
    assert isinstance(data["confidence"], (int, float))
    assert isinstance(data["revision_need"], (int, float))
    assert isinstance(data["misconception_severity"], (int, float))
    assert isinstance(data["prerequisites_ready"], bool)


def test_learning_action_priority_is_bounded():
    response = client.get("/learning-actions/100")

    assert response.status_code == 200

    priority = response.json()["priority"]

    assert 0.0 <= priority <= 1.0


def test_learning_action_signals_are_bounded():
    response = client.get("/learning-actions/100")

    assert response.status_code == 200

    data = response.json()

    assert 0.0 <= data["mastery"] <= 1.0
    assert 0.0 <= data["confidence"] <= 1.0
    assert 0.0 <= data["revision_need"] <= 1.0
    assert 0.0 <= data["misconception_severity"] <= 1.0