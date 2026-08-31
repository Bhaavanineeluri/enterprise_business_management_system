from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_audit_log():
    response = client.post(
        "/api/v1/audit-logs/",
        params={
            "action": "TEST_ACTION",
            "user_id": 1,
            "resource": "employees",
            "resource_id": "1",
            "ip_address": "127.0.0.1",
            "user_agent": "pytest",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["action"] == "TEST_ACTION"
    assert data["user_id"] == 1
    assert data["resource"] == "employees"
    assert data["resource_id"] == "1"
    assert data["ip_address"] == "127.0.0.1"
    assert data["user_agent"] == "pytest"
    assert data["created_at"] is not None


def test_get_audit_logs():
    response = client.get(
        "/api/v1/audit-logs/"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_audit_log_by_id():
    create_response = client.post(
        "/api/v1/audit-logs/",
        params={
            "action": "GET_BY_ID_TEST",
            "user_id": 1,
            "resource": "users",
            "resource_id": "1",
        },
    )

    assert create_response.status_code == 200

    audit_log_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/audit-logs/{audit_log_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == audit_log_id
    assert data["action"] == "GET_BY_ID_TEST"


def test_audit_log_details():
    response = client.post(
        "/api/v1/audit-logs/",
        params={
            "action": "DETAILS_TEST",
            "user_id": 1,
            "resource": "employees",
            "resource_id": "10",
            "details": '{"source": "pytest", "success": true}',
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["details"] is not None
