from fastapi import HTTPException, Request, status

from services.rate_limit.rate_limit_service import check_rate_limit


def rate_limit(
    limit: int = 10,
    window: int = 60,
):
    def dependency(request: Request):
        client_ip = request.client.host if request.client else "unknown"

        key = f"rate_limit:{client_ip}"

        allowed = check_rate_limit(
            key,
            limit=limit,
            window=window,
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

    return dependency
