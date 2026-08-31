from routers.v1.search.search_router import router as search_router
from routers.v1.notifications.notification_router import router as notification_router
from routers.v1.background_tasks.background_task_router import router as background_task_router
from routers.v1.exports.csv_export_router import router as csv_export_router
from routers.v1.imports.csv_import_router import router as csv_import_router
from fastapi import APIRouter

from routers.v1.employees.employee_router import router as employee_router
from routers.v1.files.file_router import router as file_router
from routers.v1.health.health_router import router as health_router
from routers.v1.users.user_router import router as user_router
from routers.v1.audit_logs.audit_log_router import router as audit_log_router
from routers.v1.devices.device_router import router as device_router
router = APIRouter(
    prefix="/api/v1",
)


router.include_router(employee_router)
router.include_router(file_router)
router.include_router(health_router)
router.include_router(user_router)
router.include_router(csv_import_router)
router.include_router(csv_export_router)
router.include_router(background_task_router)
router.include_router(notification_router)
router.include_router(audit_log_router)
router.include_router(device_router)
router.include_router(search_router)
