from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_search_users():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "admin",
            "type": "user",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert "page" in data
    assert "page_size" in data
    assert "total" in data
    assert "total_pages" in data

    assert data["page"] == 1
    assert data["page_size"] == 20

    for result in data["results"]:
        assert result["type"] == "user"


def test_search_employees():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "employee",
            "type": "employee",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "results" in data

    for result in data["results"]:
        assert result["type"] == "employee"


def test_search_pagination():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "a",
            "type": "user",
            "page": 1,
            "page_size": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 1

    assert len(data["results"]) <= 1


def test_search_sort_order_asc():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "a",
            "type": "user",
            "sort_order": "asc",
        },
    )

    assert response.status_code == 200


def test_search_sort_order_desc():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "a",
            "type": "user",
            "sort_order": "desc",
        },
    )

    assert response.status_code == 200


def test_search_invalid_type():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "admin",
            "type": "invalid",
        },
    )

    assert response.status_code == 422


def test_search_invalid_page():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "admin",
            "type": "user",
            "page": 0,
        },
    )

    assert response.status_code == 422


def test_search_invalid_page_size():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "admin",
            "type": "user",
            "page_size": 101,
        },
    )

    assert response.status_code == 422


def test_search_empty_query():
    response = client.get(
        "/api/v1/search/",
        params={
            "q": "",
            "type": "user",
        },
    )

    assert response.status_code == 422
