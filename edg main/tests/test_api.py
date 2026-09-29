from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation_qa():
    response = client.post("/api/qa", json={"question": ""})
    assert response.status_code == 422


def test_validation_quiz():
    response = client.post("/api/quiz", json={"text": ""})
    assert response.status_code == 422
