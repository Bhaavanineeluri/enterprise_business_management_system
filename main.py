from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from config.settings import settings
from routers.v1.router import router as v1_router
from routers.v1.exception_testing_router import router as exception_test_router
from routers.v2.router import router as v2_router

from exceptions import BusinessException
from exception_handlers import (
    business_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    unexpected_exception_handler,
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Business Management System API",
)


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
