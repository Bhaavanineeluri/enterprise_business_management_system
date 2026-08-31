from datetime import datetime

from sqlalchemy.orm import Session

from exceptions import ResourceNotFoundException
from models.notifications.notification import Notification
from schemas.notifications.notification import NotificationCreate


def create_notification(
    db: Session,
    notification_data: NotificationCreate,
) -> Notification:

    notification = Notification(
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        is_read=False,
    )

    try:
        db.add(notification)
        db.commit()
        db.refresh(notification)

    except Exception:
        db.rollback()
        raise

    return notification


def get_notification(
    db: Session,
    notification_id: int,
) -> Notification:

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id
        )
        .first()
    )

    if notification is None:
        raise ResourceNotFoundException(
            "Notification not found"
        )

    return notification


def get_user_notifications(
    db: Session,
    user_id: int,
    unread_only: bool = False,
) -> tuple[list[Notification], int]:

    query = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id
        )
    )

    if unread_only:
        query = query.filter(
            Notification.is_read.is_(False)
        )

    total = query.count()

    notifications = (
        query
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )

    return notifications, total


def mark_notification_as_read(
    db: Session,
    notification_id: int,
    user_id: int,
) -> Notification:

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        )
        .first()
    )

    if notification is None:
        raise ResourceNotFoundException(
            "Notification not found"
        )

    if not notification.is_read:
        notification.is_read = True
        notification.read_at = datetime.now()

        try:
            db.commit()
            db.refresh(notification)

        except Exception:
            db.rollback()
            raise

    return notification


def delete_notification(
    db: Session,
    notification_id: int,
    user_id: int,
) -> None:

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        )
        .first()
    )

    if notification is None:
        raise ResourceNotFoundException(
            "Notification not found"
        )

    try:
        db.delete(notification)
        db.commit()

    except Exception:
        db.rollback()
        raise
