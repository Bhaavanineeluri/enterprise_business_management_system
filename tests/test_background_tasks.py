from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from tasks.email_tasks import EMAIL_LOG_FILE
from tasks.notification_tasks import NOTIFICATION_LOG_FILE


client = TestClient(app)


def test_send_email_background_task():
    EMAIL_LOG_FILE.unlink(missing_ok=True)

    response = client.post(
        "/api/v1/background-tasks/email",
        json={
            "recipient": "test@example.com",
            "subject": "Background Test",
            "message": "This is a background email test",
        },
    )

    assert response.status_code == 202

    data = response.json()

    assert data["success"] is True
    assert (
        data["message"]
        == "Email scheduled for background processing"
    )

    assert EMAIL_LOG_FILE.exists()

    content = EMAIL_LOG_FILE.read_text(
        encoding="utf-8"
    )

    assert "test@example.com" in content
    assert "Background Test" in content


def test_create_notification_background_task():
    NOTIFICATION_LOG_FILE.unlink(
        missing_ok=True
    )

    response = client.post(
        "/api/v1/background-tasks/notification",
        json={
            "user_id": 1,
            "message": "Background notification test",
        },
    )

    assert response.status_code == 202

    data = response.json()

    assert data["success"] is True
    assert (
        data["message"]
        == "Notification scheduled for background processing"
    )

    assert NOTIFICATION_LOG_FILE.exists()

    content = NOTIFICATION_LOG_FILE.read_text(
        encoding="utf-8"
    )

    assert "USER_ID=1" in content
    assert "Background notification test" in content


def test_background_email_validation():
    response = client.post(
        "/api/v1/background-tasks/email",
        json={
            "recipient": "invalid-email",
            "subject": "Test",
            "message": "Test message",
        },
    )

    assert response.status_code == 422


def test_background_notification_validation():
    response = client.post(
        "/api/v1/background-tasks/notification",
        json={
            "user_id": 0,
            "message": "Test notification",
        },
    )

    assert response.status_code == 422
