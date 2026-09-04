import time

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint_response_time():
    start_time = time.perf_counter()

    response = client.get("/health")

    elapsed_time = time.perf_counter() - start_time

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    assert elapsed_time < 1.0


def test_health_endpoint_average_response_time():
    response_times = []

    for _ in range(10):
        start_time = time.perf_counter()

        response = client.get("/health")

        elapsed_time = time.perf_counter() - start_time
        response_times.append(elapsed_time)

        assert response.status_code == 200

    average_time = sum(response_times) / len(response_times)

    print(f"\nAverage response time: {average_time:.4f} seconds")

    assert average_time < 1.0


def test_database_health_endpoint_response_time():
    start_time = time.perf_counter()

    response = client.get("/api/v1/health/database")

    elapsed_time = time.perf_counter() - start_time

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "connected"

    print(f"\nDatabase health response time: {elapsed_time:.4f} seconds")

    assert elapsed_time < 1.0


def test_database_health_average_response_time():
    response_times = []

    for _ in range(10):
        start_time = time.perf_counter()

        response = client.get("/api/v1/health/database")

        elapsed_time = time.perf_counter() - start_time
        response_times.append(elapsed_time)

        assert response.status_code == 200

    average_time = sum(response_times) / len(response_times)

    print(
        f"\nAverage database response time: "
        f"{average_time:.4f} seconds"
    )

    assert average_time < 1.0
