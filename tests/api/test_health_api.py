from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_monitoring_api():
    response = client.get("/api/v1/health-monitoring/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"]["status"] == "healthy"
    assert data["redis"]["status"] == "healthy"
