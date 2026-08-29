from fastapi import APIRouter

from routers.v1.employees.employee_router import router as employee_router
from routers.v1.health.health_router import router as health_router


router = APIRouter(
    prefix="/api/v1",
)


router.include_router(health_router)
router.include_router(employee_router)
