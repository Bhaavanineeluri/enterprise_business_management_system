from fastapi import APIRouter

from services.redis.redis_service import (
    set_temporary_data,
    get_temporary_data,
    delete_temporary_data,
)

router = APIRouter(
    prefix="/redis",
    tags=["Redis"],
)


@router.post("/test")
def test_redis():
    key = "ebms:module41:test"

    set_temporary_data(
        key,
        "Redis integration working",
        expiration=60,
    )

    value = get_temporary_data(key)

    return {
        "key": key,
        "value": value,
        "status": "Redis is working",
    }


@router.delete("/test")
def delete_redis_test():
    key = "ebms:module41:test"

    deleted = delete_temporary_data(key)

    return {
        "deleted": deleted > 0,
    }
