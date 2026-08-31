
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.devices.device import DeviceCreate, DeviceResponse
from services.devices.device_service import (
    create_device,
    get_active_device,
    get_user_devices,
    revoke_device,
    update_device_login,
)


router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.post(
    "/",
    response_model=DeviceResponse,
)
def create_device_endpoint(
    device_data: DeviceCreate,
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
):
    return create_device(
        db=db,
        user_id=user_id,
        device_id=device_data.device_id,
        device_name=device_data.device_name,
        device_type=device_data.device_type,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )


@router.get(
    "/",
    response_model=list[DeviceResponse],
)
def get_user_devices_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_devices(
        db=db,
        user_id=user_id,
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_active_device_endpoint(
    device_id: str,
    user_id: int,
    db: Session = Depends(get_db),
):
    device = get_active_device(
        db=db,
        user_id=user_id,
        device_id=device_id,
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Active device not found",
        )

    return device


@router.delete(
    "/{device_id}",
)
def revoke_device_endpoint(
    device_id: str,
    user_id: int,
    db: Session = Depends(get_db),
):
    revoked = revoke_device(
        db=db,
        user_id=user_id,
        device_id=device_id,
    )

    if not revoked:
        raise HTTPException(
            status_code=404,
            detail="Active device not found",
        )

    return {
        "message": "Device revoked successfully",
    }


@router.patch(
    "/{device_id}/login",
    response_model=DeviceResponse,
)
def update_device_login_endpoint(
    device_id: str,
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    device = get_active_device(
        db=db,
        user_id=user_id,
        device_id=device_id,
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Active device not found",
        )

    return update_device_login(
        db=db,
        device=device,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

