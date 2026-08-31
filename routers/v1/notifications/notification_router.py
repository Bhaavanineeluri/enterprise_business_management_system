from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies.auth import get_current_user
from dependencies.database import get_db
from models.users.user import User
from schemas.notifications.notification import (
    NotificationCreate,
    NotificationListData,
    NotificationListResponse,
    NotificationMessageResponse,
)
from services.notifications.notification_service import (
    create_notification,
    delete_notification,
    get_user_notifications,
    mark_notification_as_read,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post(
    "",
    response_model=NotificationMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification_api(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = create_notification(
        db=db,
        notification_data=notification_data,
    )

    return {
        "success": True,
        "message": "Notification created successfully",
        "data": notification,
    }


@router.get(
    "",
    response_model=NotificationListResponse,
)
def get_notifications_api(
    unread_only: bool = Query(
        default=False,
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notifications, total = get_user_notifications(
        db=db,
        user_id=current_user.id,
        unread_only=unread_only,
    )

    return {
        "success": True,
        "message": "Notifications retrieved successfully",
        "data": {
            "items": notifications,
            "total": total,
        },
    }


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationMessageResponse,
)
def mark_notification_read_api(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = mark_notification_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id,
    )

    return {
        "success": True,
        "message": "Notification marked as read",
        "data": notification,
    }


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification_api(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id,
    )

    return None
