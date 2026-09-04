from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_external_api_success():
    mock_result = {
        "success": True,
        "status_code": 200,
        "data": {
            "id": 1,
            "name": "Test User",
        },
    }

    with patch(
        "routers.v1.external_api.external_api_router.call_external_api",
        return_value=mock_result,
    ):
        response = client.get(
            "/api/v1/external-api/call",
            params={"url": "https://example.com"},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["status_code"] == 200
    assert data["data"]["id"] == 1


def test_external_api_failure():
    mock_result = {
        "success": False,
        "status_code": 502,
        "error": "Unable to connect to external API",
    }

    with patch(
        "routers.v1.external_api.external_api_router.call_external_api",
        return_value=mock_result,
    ):
        response = client.get(
            "/api/v1/external-api/call",
            params={"url": "https://example.com"},
        )

    assert response.status_code == 502

    data = response.json()

    assert data["message"] == "Unable to connect to external API"
