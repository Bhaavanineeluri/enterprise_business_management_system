from routers.v1.search.search_router import router as search_router
from routers.v1.notifications.notification_router import router as notification_router
from routers.v1.background_tasks.background_task_router import router as background_task_router
from routers.v1.exports.csv_export_router import router as csv_export_router
from routers.v1.imports.csv_import_router import router as csv_import_router
from fastapi import APIRouter
from routers.v1.webhooks.webhook_router import router as webhook_router
from routers.v1.rate_limit_test_router import router as rate_limit_test_router

from routers.v1.employees.employee_router import router as employee_router
from routers.v1.customers.customer_router import router as customer_router
from routers.v1.products.product_router import router as product_router
from routers.v1.orders.order_router import router as order_router
from routers.v1.payments.payment_router import router as payment_router
from routers.v1.files.file_router import router as file_router
from routers.v1.health.health_router import router as health_router
from routers.v1.users.user_router import router as user_router
from routers.v1.audit_logs.audit_log_router import router as audit_log_router
from routers.v1.devices.device_router import router as device_router
from routers.v1.record_history.record_history_router import router as record_history_router
from routers.v1.redis.redis_router import router as redis_router
from routers.v1.external_api.external_api_router import router as external_api_router
from routers.v1.async_processing.async_router import router as async_processing_router
from routers.v1.concurrent_operations.concurrent_router import router as concurrent_operations_router
from routers.v1.health_monitoring.health_router import router as health_monitoring_router
router = APIRouter(
    prefix="/api/v1",
)


router.include_router(employee_router)
router.include_router(customer_router)
router.include_router(product_router)
router.include_router(order_router)
router.include_router(payment_router)
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

router.include_router(record_history_router)

router.include_router(redis_router)

router.include_router(rate_limit_test_router)

router.include_router(webhook_router)

router.include_router(external_api_router)


router.include_router(async_processing_router)

router.include_router(concurrent_operations_router)

router.include_router(health_monitoring_router)
