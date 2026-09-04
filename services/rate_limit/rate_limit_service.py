from services.redis.redis_service import redis_client


def check_rate_limit(
    key: str,
    limit: int = 10,
    window: int = 60,
) -> bool:
    current_count = redis_client.incr(key)

    if current_count == 1:
        redis_client.expire(key, window)

    return current_count <= limit
