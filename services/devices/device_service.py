from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.devices.device import Device
from models.sessions.session import UserSession


def create_device(
    db: Session,
    user_id: int,
    device_id: str,
    device_name: str | None = None,
    device_type: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> Device:

    device = Device(
        user_id=user_id,
        device_id=device_id,
        device_name=device_name,
        device_type=device_type,
        ip_address=ip_address,
        user_agent=user_agent,
        is_active=True,
        last_login_at=datetime.now(timezone.utc).replace(
            tzinfo=None
        ),
    )

    try:
        db.add(device)
        db.commit()
        db.refresh(device)

    except Exception:
        db.rollback()
        raise

    return device


def get_user_devices(
    db: Session,
    user_id: int,
) -> list[Device]:

    return (
        db.query(Device)
        .filter(
            Device.user_id == user_id,
        )
        .order_by(Device.created_at.desc())
        .all()
    )


def get_active_device(
    db: Session,
    user_id: int,
    device_id: str,
) -> Device | None:

    return (
        db.query(Device)
        .filter(
            Device.user_id == user_id,
            Device.device_id == device_id,
            Device.is_active.is_(True),
        )
        .first()
    )


def revoke_device(
    db: Session,
    user_id: int,
    device_id: str,
) -> bool:

    device = (
        db.query(Device)
        .filter(
            Device.user_id == user_id,
            Device.device_id == device_id,
            Device.is_active.is_(True),
        )
        .first()
    )

    if device is None:
        return False

    device.is_active = False

    now = datetime.now()

    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active.is_(True),
    ).update(
        {
            UserSession.is_active: False,
            UserSession.revoked_at: now,
        },
        synchronize_session=False,
    )

    db.commit()

    return True


def update_device_login(
    db: Session,
    device: Device,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> Device:

    device.last_login_at = datetime.now(
        timezone.utc
    ).replace(tzinfo=None)

    if ip_address is not None:
        device.ip_address = ip_address

    if user_agent is not None:
        device.user_agent = user_agent

    device.is_active = True

    db.commit()
    db.refresh(device)

    return device
