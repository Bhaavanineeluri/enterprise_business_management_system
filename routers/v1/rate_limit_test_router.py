from fastapi import APIRouter, Depends

from dependencies.rate_limit import rate_limit

router = APIRouter(
    prefix="/rate-limit-test",
    tags=["Rate Limit Test"],
)


@router.get(
    "/",
    dependencies=[Depends(rate_limit(limit=3, window=60))],
)
def rate_limit_test():
    return {
        "message": "Request allowed",
    }
