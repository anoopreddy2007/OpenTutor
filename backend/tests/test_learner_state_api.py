from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_user_learner_states():
    response = client.get("/learner-states/user/1")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_learner_state_for_concept():
    response = client.get("/learner-states/user/1/concept/1")

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert data["concept_id"] == 1
    assert "mastery" in data
    assert "confidence" in data
    assert "attempts_count" in data
    assert "correct_count" in data


def test_learner_state_user_not_found():
    response = client.get("/learner-states/user/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_learner_state_concept_not_found():
    response = client.get(
        "/learner-states/user/1/concept/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Concept not found"