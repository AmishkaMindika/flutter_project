from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_progress():
    response = client.post("/api/progress/", json={"user_id": 1, "day": "Monday", "score": 80})
    assert response.status_code == 200

def test_get_progress():
    response = client.get("/api/progress/1")
    assert response.status_code in [200, 404]
