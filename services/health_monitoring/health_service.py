from database import engine
from services.redis.redis_service import redis_client


def check_database() -> dict:
    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")

        return {
            "status": "healthy",
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "error": str(exc),
        }


def check_redis() -> dict:
    try:
        redis_client.ping()

        return {
            "status": "healthy",
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "error": str(exc),
        }


def get_health_status() -> dict:
    database = check_database()
    redis = check_redis()

    overall_status = (
        "healthy"
        if database["status"] == "healthy"
        and redis["status"] == "healthy"
        else "unhealthy"
    )

    return {
        "status": overall_status,
        "database": database,
        "redis": redis,
    }
