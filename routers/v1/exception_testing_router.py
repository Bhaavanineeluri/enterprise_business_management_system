from fastapi import APIRouter, HTTPException

from exceptions import (
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
    PermissionDeniedException,
)


router = APIRouter(
    prefix="/api/v1/test-exceptions",
    tags=["Exception Testing"],
)


@router.get("/business")
def test_business_exception():
    raise ResourceNotFoundException("Test resource was not found")


@router.get("/duplicate")
def test_duplicate_exception():
    raise ResourceAlreadyExistsException("Test resource already exists")


@router.get("/permission")
def test_permission_exception():
    raise PermissionDeniedException("Test permission denied")


@router.get("/http")
def test_http_exception():
    raise HTTPException(
        status_code=400,
        detail="Test HTTP exception",
    )


@router.get("/unexpected")
def test_unexpected_exception():
    raise RuntimeError("Test unexpected exception")
