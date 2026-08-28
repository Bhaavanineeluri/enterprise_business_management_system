from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1",
)


@router.get("/health")
def api_health_check():
    return {
        "status": "healthy",
        "version": "v1",
    }
