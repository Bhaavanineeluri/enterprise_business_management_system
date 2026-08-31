from sqlalchemy.orm import Session

from exceptions import ResourceNotFoundException
from models.users.user import User
from schemas.users.user import UserCreate, UserLogin
from security.password import hash_password, verify_password


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username is not None:
        from exceptions import ResourceAlreadyExistsException

        raise ResourceAlreadyExistsException(
            "Username already exists"
        )

    existing_email = (
        db.query(User)
        .filter(User.email == str(user_data.email))
        .first()
    )

    if existing_email is not None:
        from exceptions import ResourceAlreadyExistsException

        raise ResourceAlreadyExistsException(
            "Email already exists"
        )

    user = User(
        username=user_data.username,
        email=str(user_data.email),
        hashed_password=hash_password(user_data.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise

    return user


def authenticate_user(
    db: Session,
    login_data: UserLogin,
) -> User:

    from datetime import datetime, timedelta

    from config.settings import settings

    user = (
        db.query(User)
        .filter(User.username == login_data.username)
        .first()
    )

    if user is None:
        raise ResourceNotFoundException(
            "Invalid username or password"
        )

    if not user.is_active:
        raise ResourceNotFoundException(
            "User account is inactive"
        )

    now = datetime.now()

    if user.locked_until is not None:

        if user.locked_until > now:
            raise ResourceNotFoundException(
                "User account is temporarily locked"
            )

        user.locked_until = None
        user.failed_login_attempts = 0

    if not verify_password(
        login_data.password,
        user.hashed_password,
    ):

        user.failed_login_attempts += 1

        if (
            user.failed_login_attempts
            >= settings.MAX_LOGIN_ATTEMPTS
        ):
            user.locked_until = (
                now
                + timedelta(
                    minutes=settings.ACCOUNT_LOCK_MINUTES
                )
            )

        db.commit()

        if user.locked_until is not None:
            raise ResourceNotFoundException(
                "User account is temporarily locked"
            )

        raise ResourceNotFoundException(
            "Invalid username or password"
        )

    user.failed_login_attempts = 0
    user.locked_until = None

    db.commit()
    db.refresh(user)

    return user
