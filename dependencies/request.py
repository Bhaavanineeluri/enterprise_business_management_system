from fastapi import Request


def get_request_id(request: Request) -> str | None:
    return request.headers.get("X-Request-ID")
