from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.pagination import pagination_params
from dependencies.request import get_request_id


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "version": "v1",
    }


@router.get("/database")
def database_health_check(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }


@router.get("/dependency-demo")
def dependency_demo(
    request_id: str | None = Depends(get_request_id),
    pagination: dict[str, int] = Depends(pagination_params),
):
    return {
        "request_id": request_id,
        "pagination": pagination,
    }
