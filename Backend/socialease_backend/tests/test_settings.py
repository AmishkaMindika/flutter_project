from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_settings():
    response = client.get("/api/settings/1")
    assert response.status_code in [200, 404]
