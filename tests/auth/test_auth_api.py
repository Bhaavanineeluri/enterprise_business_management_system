import uuid

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_user():
    unique_id = uuid.uuid4().hex[:8]

    username = f"apitest_{unique_id}"
    email = f"apitest_{unique_id}@example.com"

    response = client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "User registered successfully"
    assert data["data"]["username"] == username
    assert data["data"]["email"] == email


def test_login_user():
    unique_id = uuid.uuid4().hex[:8]

    username = f"loginuser_{unique_id}"
    email = f"loginuser_{unique_id}@example.com"

    register_response = client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/api/v1/users/login",
        json={
            "username": username,
            "password": "Test@12345",
            "device_id": f"test-device-{unique_id}",
            "device_name": "Test Mac",
            "device_type": "desktop",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Login successful"
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_invalid_password():
    unique_id = uuid.uuid4().hex[:8]

    username = f"invalidpw_{unique_id}"
    email = f"invalidpw_{unique_id}@example.com"

    register_response = client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/api/v1/users/login",
        json={
            "username": username,
            "password": "WrongPassword123",
            "device_id": f"invalid-device-{unique_id}",
            "device_name": "Test Mac",
            "device_type": "desktop",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"]


def test_account_lockout():
    unique_id = uuid.uuid4().hex[:8]

    username = f"lockout_{unique_id}"
    email = f"lockout_{unique_id}@example.com"

    register_response = client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert register_response.status_code == 201

    login_payload = {
        "username": username,
        "password": "WrongPassword123",
        "device_id": f"lockout-device-{unique_id}",
        "device_name": "Test Mac",
        "device_type": "desktop",
    }

    for _ in range(5):
        response = client.post(
            "/api/v1/users/login",
            json=login_payload,
        )

    assert response.status_code == 404
    assert "temporarily locked" in response.json()["message"].lower()

    response = client.post(
        "/api/v1/users/login",
        json={
            "username": username,
            "password": "Test@12345",
            "device_id": f"lockout-device-{unique_id}",
            "device_name": "Test Mac",
            "device_type": "desktop",
        },
    )

    assert response.status_code == 404
    assert "temporarily locked" in response.json()["message"].lower()


def test_login_invalid_username():
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/api/v1/users/login",
        json={
            "username": f"nonexistent_{unique_id}",
            "password": "Test@12345",
            "device_id": f"invalid-user-device-{unique_id}",
            "device_name": "Test Mac",
            "device_type": "desktop",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Invalid username or password"


def test_get_current_user_without_token():
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401

    data = response.json()

    assert data["message"]


def test_get_current_user_with_invalid_token():
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["message"]


def test_get_current_user_with_valid_token():
    unique_id = uuid.uuid4().hex[:8]

    username = f"meuser_{unique_id}"
    email = f"meuser_{unique_id}@example.com"

    register_response = client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        json={
            "username": username,
            "password": "Test@12345",
            "device_id": f"me-device-{unique_id}",
            "device_name": "Test Mac",
            "device_type": "desktop",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == username
    assert data["email"] == email


def test_logout_user():
    unique_id = uuid.uuid4().hex[:8]

    username = f"logout_{unique_id}"
    email = f"logout_{unique_id}@example.com"

    register_response = client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        json={
            "username": username,
            "password": "Test@12345",
            "device_id": f"logout-device-{unique_id}",
            "device_name": "Test Mac",
            "device_type": "desktop",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/users/logout",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True


def test_revoked_token_cannot_access_current_user():
    unique_id = uuid.uuid4().hex[:8]

    username = f"revoked_{unique_id}"
    email = f"revoked_{unique_id}@example.com"

    register_response = client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        json={
            "username": username,
            "password": "Test@12345",
            "device_id": f"revoked-device-{unique_id}",
            "device_name": "Test Mac",
            "device_type": "desktop",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    logout_response = client.post(
        "/api/v1/users/logout",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert logout_response.status_code == 200

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["message"]
