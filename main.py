from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from middleware.request_middleware import request_middleware
from middleware.security_headers import security_headers_middleware
from config.settings import settings
from middleware.request_middleware import request_middleware
from routers.v1.router import router as v1_router
from routers.v1.exception_testing_router import router as exception_test_router
from routers.v2.router import router as v2_router

from exceptions import BusinessException
from scheduler.scheduler import start_scheduler, stop_scheduler
from exception_handlers import (
    business_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    unexpected_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


openapi_tags = [
    {"name": "Authentication", "description": "User registration, login, logout, and password recovery APIs."},

    {"name": "Users", "description": "Current user and user management APIs."},
    {"name": "Employees", "description": "Employee management APIs."},
    {"name": "Customers", "description": "Customer management APIs."},
    {"name": "Products", "description": "Product and inventory management APIs."},
    {"name": "Orders", "description": "Order management APIs."},
    {"name": "Payments", "description": "Payment management APIs."},
    {"name": "Tasks", "description": "Task management APIs."},
    {"name": "Notifications", "description": "Notification management APIs."},
    {"name": "Reports", "description": "Report management APIs."},
    {"name": "Files", "description": "File upload, download, and management APIs."},
    {"name": "Audit Logs", "description": "Audit logging APIs."},
    {"name": "Record History", "description": "Historical record tracking APIs."},
    {"name": "Devices", "description": "Device registration and management APIs."},
    {"name": "Health", "description": "Application and database health APIs."},
    {"name": "Health Monitoring", "description": "System health monitoring APIs."},
    {"name": "Search", "description": "Global search APIs."},
    {"name": "CSV Import", "description": "CSV import APIs."},
    {"name": "CSV Export", "description": "CSV export APIs."},
    {"name": "Background Tasks", "description": "Background task APIs."},
    {"name": "Redis", "description": "Redis integration APIs."},
    {"name": "Webhooks", "description": "Webhook management and delivery APIs."},
    {"name": "External API", "description": "External API integration APIs."},
    {"name": "AsyncProcessing", "description": "Asynchronous processing APIs."},
    {"name": "Concurrent Operations", "description": "Concurrent operation APIs."},
    {"name": "Rate Limit Test", "description": "Rate limiting test APIs."},
    {"name": "Exception Testing", "description": "Exception handling test APIs."},
    {"name": "Health V2", "description": "Version 2 health APIs."},
]

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Business Management System API",
    openapi_tags=openapi_tags,
    lifespan=lifespan,
)


app.middleware("http")(request_middleware)
#app.middleware("http")(security_headers_middleware)
app.add_exception_handler(
    BusinessException,
    business_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)



@app.get("/")
def root():
    return {
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


app.include_router(exception_test_router)
app.include_router(v1_router)
app.include_router(v2_router)
