from fastapi import APIRouter, status

from services.health_monitoring.health_service import get_health_status


router = APIRouter(
    prefix="/health-monitoring",
    tags=["Health Monitoring"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
def health_monitoring():
    return get_health_status()
