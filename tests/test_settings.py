import os
import subprocess
import sys


def run_settings_with_environment(environment: str):
    env = os.environ.copy()
    env["ENVIRONMENT"] = environment

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from config.settings import settings; "
                "print(settings.ENVIRONMENT); "
                "print(settings.is_production)"
            ),
        ],
        env=env,
        capture_output=True,
        text=True,
    )

    return result


def test_development_environment():
    result = run_settings_with_environment(
        "development"
    )

    assert result.returncode == 0
    assert "development" in result.stdout
    assert "False" in result.stdout


def test_testing_environment():
    result = run_settings_with_environment(
        "testing"
    )

    assert result.returncode == 0
    assert "testing" in result.stdout
    assert "False" in result.stdout


def test_production_environment():
    result = run_settings_with_environment(
        "production"
    )

    assert result.returncode == 0
    assert "production" in result.stdout
    assert "True" in result.stdout


def test_invalid_environment():
    result = run_settings_with_environment(
        "invalid_environment"
    )

    assert result.returncode != 0


def test_invalid_database_port():
    env = os.environ.copy()
    env["ENVIRONMENT"] = "development"
    env["DB_PORT"] = "99999"

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from config.settings import settings",
        ],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0


def test_weak_jwt_secret_rejected():
    import pytest
    from config.settings import Settings

    with pytest.raises(ValueError, match="JWT_SECRET_KEY must be at least 32 characters"):
        Settings(
            APP_NAME="Test",
            APP_VERSION="1.0",
            ENVIRONMENT="testing",
            DB_HOST="localhost",
            DB_PORT=3306,
            DB_USER="root",
            DB_PASSWORD="password",
            DB_NAME="test",
            JWT_SECRET_KEY="short-secret",
            ENCRYPTION_KEY="test-encryption-key",
        )
