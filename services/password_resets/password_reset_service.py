from datetime import datetime, timedelta
import hashlib
import secrets

from sqlalchemy.orm import Session

from config.settings import settings
from exceptions import ResourceNotFoundException
from models.password_resets.password_reset import PasswordReset
from models.users.user import User
from security.password import hash_password


def create_password_reset_token(
    db: Session,
    email: str,
) -> str:

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise ResourceNotFoundException(
            "User not found"
        )

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    expires_at = (
        datetime.now()
        + timedelta(
            minutes=settings.PASSWORD_RESET_MINUTES
        )
    )

    reset = PasswordReset(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        used=False,
    )

    try:
        db.add(reset)
        db.commit()
        db.refresh(reset)

    except Exception:
        db.rollback()
        raise

    return token


def reset_password(
    db: Session,
    token: str,
    new_password: str,
) -> None:

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    reset = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.token_hash == token_hash,
            PasswordReset.used.is_(False),
        )
        .first()
    )

    if reset is None:
        raise ResourceNotFoundException(
            "Invalid or already used reset token"
        )

    if reset.expires_at < datetime.now():
        raise ResourceNotFoundException(
            "Reset token has expired"
        )

    user = (
        db.query(User)
        .filter(User.id == reset.user_id)
        .first()
    )

    if user is None:
        raise ResourceNotFoundException(
            "User not found"
        )

    user.hashed_password = hash_password(
        new_password
    )

    reset.used = True

    db.commit()
