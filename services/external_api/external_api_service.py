import httpx


def call_external_api(
    url: str,
    timeout: float = 10.0,
) -> dict:

    try:
        response = httpx.get(
            url,
            timeout=timeout,
        )

        response.raise_for_status()

        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json(),
        }

    except httpx.TimeoutException:
        return {
            "success": False,
            "status_code": 504,
            "error": "External API request timed out",
        }

    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "status_code": exc.response.status_code,
            "error": "External API returned an HTTP error",
        }

    except httpx.RequestError:
        return {
            "success": False,
            "status_code": 502,
            "error": "Unable to connect to external API",
        }

    except ValueError:
        return {
            "success": False,
            "status_code": 502,
            "error": "External API returned invalid JSON",
        }
