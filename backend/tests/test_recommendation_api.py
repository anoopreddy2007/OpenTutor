from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_next_recommendation():
    response = client.get("/recommendations/next/1")

    assert response.status_code == 200

    data = response.json()

    assert "concept_id" in data


def test_recommendation_user_not_found():
    response = client.get("/recommendations/next/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"