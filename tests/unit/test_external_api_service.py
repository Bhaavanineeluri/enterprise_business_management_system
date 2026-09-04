from unittest.mock import Mock, patch

from services.external_api.external_api_service import call_external_api


def test_call_external_api_success():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Test User",
    }

    with patch(
        "services.external_api.external_api_service.httpx.get",
        return_value=mock_response,
    ):
        result = call_external_api("https://example.com")

    assert result["success"] is True
    assert result["status_code"] == 200
    assert result["data"]["id"] == 1


def test_call_external_api_timeout():
    import httpx

    with patch(
        "services.external_api.external_api_service.httpx.get",
        side_effect=httpx.TimeoutException("Request timed out"),
    ):
        result = call_external_api("https://example.com")

    assert result["success"] is False
    assert result["status_code"] == 504
    assert result["error"] == "External API request timed out"


def test_call_external_api_http_error():
    import httpx

    mock_response = Mock()
    mock_response.status_code = 500

    request = httpx.Request(
        "GET",
        "https://example.com",
    )

    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Internal Server Error",
        request=request,
        response=mock_response,
    )

    with patch(
        "services.external_api.external_api_service.httpx.get",
        return_value=mock_response,
    ):
        result = call_external_api("https://example.com")

    assert result["success"] is False
    assert result["status_code"] == 500
    assert result["error"] == "External API returned an HTTP error"


def test_call_external_api_request_error():
    import httpx

    with patch(
        "services.external_api.external_api_service.httpx.get",
        side_effect=httpx.RequestError("Connection failed"),
    ):
        result = call_external_api("https://example.com")

    assert result["success"] is False
    assert result["status_code"] == 502
    assert result["error"] == "Unable to connect to external API"


def test_call_external_api_invalid_json():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")

    with patch(
        "services.external_api.external_api_service.httpx.get",
        return_value=mock_response,
    ):
        result = call_external_api("https://example.com")

    assert result["success"] is False
    assert result["status_code"] == 502
    assert result["error"] == "External API returned invalid JSON"
