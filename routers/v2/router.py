from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from routers.v2.health.health_router import router as health_router


router = APIRouter(
    prefix="/api/v2",
)


router.include_router(health_router)
