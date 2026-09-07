from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from config.settings import settings
from dependencies.auth import get_current_user
from dependencies.database import get_db
from dependencies.permission import require_permission
from schemas.password_resets.password_reset import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)
from schemas.users.user import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserRegistrationResponse,
    UserResponse,
)
from security.jwt import create_access_token
from services.audit_logs.audit_log_service import create_audit_log
from services.devices.device_service import (
    get_user_devices,
    revoke_device,
)
from services.password_resets.password_reset_service import (
    create_password_reset_token,
    reset_password,
)
from services.sessions.session_service import (
    create_session,
    revoke_all_sessions,
    revoke_session,
)
from services.users.user_service import (
    authenticate_user,
    create_user,
)


security = HTTPBearer()

router = APIRouter(
    prefix="/users",
)


# =========================
# Authentication
# =========================

@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
)
def register_user_api(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    user = create_user(
        db,
        user_data,
    )

    return {
        "success": True,
        "message": "User registered successfully",
        "data": user,
    }


@router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
def login_user_api(
    login_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        login_data,
    )

    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    expires_at = datetime.now(timezone.utc).replace(
        tzinfo=None
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    session = create_session(
        db=db,
        user_id=user.id,
        session_token="pending",
        expires_at=expires_at,
    )

    access_token = create_access_token(
        user_id=user.id,
        username=user.username,
        session_id=str(session.id),
    )

    session.session_token = access_token
    db.commit()

    create_audit_log(
        db=db,
        user_id=user.id,
        action="LOGIN_SUCCESS",
        resource="users",
        resource_id=str(user.id),
        ip_address=client_ip,
        user_agent=user_agent,
        details={
            "login_method": "username_password",
        },
    )

    return {
        "success": True,
        "message": "Login successful",
        "data": user,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
def logout_user_api(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    success = revoke_session(
        db=db,
        session_token=token,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or already revoked",
        )

    return {
        "success": True,
        "message": "Logout successful",
    }


@router.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
def logout_all_users_api(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    count = revoke_all_sessions(
        db=db,
        user_id=current_user.id,
    )

    return {
        "success": True,
        "message": "All sessions logged out successfully",
        "sessions_revoked": count,
    }


@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
def forgot_password_api(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    token = create_password_reset_token(
        db,
        str(request.email),
    )

    return {
        "success": True,
        "message": "Password reset token generated successfully",
        "reset_token": token,
    }


@router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
def reset_password_api(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    reset_password(
        db,
        request.token,
        request.new_password,
    )

    return {
        "success": True,
        "message": "Password reset successfully",
    }


# =========================
# Users
# =========================

@router.get(
    "/me",
    response_model=UserResponse,
    tags=["Users"],
)
def get_current_user_api(
    current_user=Depends(get_current_user),
):
    return current_user


@router.get(
    "/admin-test",
    response_model=UserResponse,
    tags=["Users"],
)
def admin_test_api(
    current_user=Depends(
        require_permission("DELETE_USER")
    ),
):
    return current_user


# =========================
# Devices
# =========================

@router.get(
    "/devices",
    status_code=status.HTTP_200_OK,
    tags=["Devices"],
)
def get_devices_api(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    devices = get_user_devices(
        db=db,
        user_id=current_user.id,
    )

    return {
        "success": True,
        "message": "Devices retrieved successfully",
        "data": devices,
    }


@router.delete(
    "/devices/{device_id}",
    status_code=status.HTTP_200_OK,
    tags=["Devices"],
)
def revoke_device_api(
    device_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    success = revoke_device(
        db=db,
        user_id=current_user.id,
        device_id=device_id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found or already revoked",
        )

    return {
        "success": True,
        "message": "Device revoked successfully",
    }
