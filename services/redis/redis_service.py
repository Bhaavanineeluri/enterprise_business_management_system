import json

import redis

from config.settings import settings


redis_client = redis.Redis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=int(getattr(settings, "REDIS_PORT", 6379)),
    db=int(getattr(settings, "REDIS_DB", 0)),
    decode_responses=True,
)


def set_temporary_data(
    key: str,
    value: str,
    expiration: int = 300,
) -> bool:
    return redis_client.set(
        key,
        value,
        ex=expiration,
    )


def get_temporary_data(key: str) -> str | None:
    return redis_client.get(key)


def delete_temporary_data(key: str) -> int:
    return redis_client.delete(key)


def set_cached_data(
    key: str,
    value,
    expiration: int = 300,
) -> bool:
    return redis_client.set(
        key,
        json.dumps(value),
        ex=expiration,
    )


def get_cached_data(key: str):
    value = redis_client.get(key)

    if value is None:
        return None

    return json.loads(value)


def delete_cached_data(key: str) -> int:
    return redis_client.delete(key)


def invalidate_employee_cache(employee_id: int) -> int:
    return delete_cached_data(f"employee:{employee_id}")
