from uuid import UUID

from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_request_id_header():
    response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None

    UUID(request_id)


def test_execution_time_header():
    response = client.get("/health")

    assert response.status_code == 200

    execution_time = response.headers.get(
        "X-Execution-Time"
    )

    assert execution_time is not None

    execution_time_value = float(execution_time)

    assert execution_time_value >= 0


def test_unique_request_ids():
    response_1 = client.get("/health")
    response_2 = client.get("/health")

    request_id_1 = response_1.headers.get("X-Request-ID")
    request_id_2 = response_2.headers.get("X-Request-ID")

    assert request_id_1 is not None
    assert request_id_2 is not None

    assert request_id_1 != request_id_2


def test_middleware_on_exception_response():
    response = client.get(
        "/api/v1/test-exceptions/business"
    )

    assert response.status_code == 404

    assert response.headers.get("X-Request-ID") is not None
    assert response.headers.get("X-Execution-Time") is not None

    data = response.json()

    assert data["success"] is False
    assert data["error_code"] == "RESOURCE_NOT_FOUND"
