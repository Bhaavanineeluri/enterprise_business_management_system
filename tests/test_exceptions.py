from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_business_exception():
    response = client.get(
        "/api/v1/test-exceptions/business"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["error_code"] == "RESOURCE_NOT_FOUND"
    assert data["message"] == "Test resource was not found"


def test_duplicate_exception():
    response = client.get(
        "/api/v1/test-exceptions/duplicate"
    )

    assert response.status_code == 409

    data = response.json()

    assert data["success"] is False
    assert data["error_code"] == "RESOURCE_ALREADY_EXISTS"


def test_permission_exception():
    response = client.get(
        "/api/v1/test-exceptions/permission"
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["error_code"] == "PERMISSION_DENIED"


def test_http_exception():
    response = client.get(
        "/api/v1/test-exceptions/http"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error_code"] == "HTTP_ERROR"
    assert data["message"] == "Test HTTP exception"


def test_unexpected_exception():
    response = client.get(
        "/api/v1/test-exceptions/unexpected"
    )

    assert response.status_code == 500

    data = response.json()

    assert data["success"] is False
    assert data["error_code"] == "INTERNAL_SERVER_ERROR"
    assert data["message"] == "An unexpected error occurred"
