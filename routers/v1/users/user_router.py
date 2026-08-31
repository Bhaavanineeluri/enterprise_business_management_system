from fastapi import Request
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta, timezone
from config.settings import settings
from security.jwt import create_access_token
from services.sessions.session_service import create_session
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.sessions.session import UserSession
from dependencies.auth import get_current_user
from dependencies.database import get_db
from dependencies.permission import require_permission
from dependencies.permission import require_permission
from security.jwt import (
    create_access_token,
    get_access_token_expiry,
)
from services.audit_logs.audit_log_service import create_audit_log
from services.devices.device_service import (
    get_active_device,
    create_device,
    update_device_login,
    get_user_devices,
    revoke_device,
)

from services.sessions.session_service import (
    create_session,
    revoke_session,
)
from security.jwt import decode_access_token

from services.devices.device_service import (
    get_active_device,
    create_device,
    update_device_login,
)

from services.sessions.session_service import (
    create_session,
    revoke_session,
    revoke_all_sessions,
)
from schemas.password_resets.password_reset import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)

from services.password_resets.password_reset_service import (
    create_password_reset_token,
    reset_password,
)

from schemas.users.user import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserRegistrationResponse,
    UserResponse,
)

from datetime import datetime, timedelta, timezone

from config.settings import settings
from security.jwt import create_access_token
from services.sessions.session_service import create_session

from services.users.user_service import (
    authenticate_user,
    create_user,
)
security = HTTPBearer()
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/devices",
    status_code=status.HTTP_200_OK,
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


@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
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

    device = get_active_device(
        db=db,
        user_id=user.id,
        device_id=login_data.device_id,
    )

    if device is None:
        create_device(
            db=db,
            user_id=user.id,
            device_id=login_data.device_id,
            device_name=login_data.device_name,
            device_type=login_data.device_type,
            ip_address=client_ip,
            user_agent=user_agent,
        )
    else:
        update_device_login(
            db=db,
            device=device,
            ip_address=client_ip,
            user_agent=user_agent,
        )

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
            "device_id": login_data.device_id,
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
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_api(
    current_user=Depends(get_current_user),
):
    return current_user


@router.get(
    "/admin-test",
    response_model=UserResponse,
)
def admin_test_api(
    current_user=Depends(
        require_permission("DELETE_USER")
    ),
):
    return current_user




@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
    status_code=status.HTTP_200_OK,
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
