from fastapi import APIRouter

from routers.v2.health.health_router import router as health_router


router = APIRouter(
    prefix="/api/v2",
)


router.include_router(health_router)
