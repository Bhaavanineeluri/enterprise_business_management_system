from datetime import datetime

from database import SessionLocal
from models.users.user import User
from security.password import hash_password
from services.users.user_service import authenticate_user
from schemas.users.user import UserLogin


def test_account_security_fields():
    db = SessionLocal()

    try:
        user = User(
            username="security_test_user",
            email="security_test@example.com",
            hashed_password=hash_password("TestPass123"),
            is_active=True,
            failed_login_attempts=0,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.failed_login_attempts == 0
        assert user.locked_until is None

    finally:
        db.query(User).filter(
            User.username == "security_test_user"
        ).delete()
        db.commit()
        db.close()


def test_locked_account():
    db = SessionLocal()

    try:
        user = User(
            username="locked_test_user",
            email="locked_test@example.com",
            hashed_password=hash_password("TestPass123"),
            is_active=True,
            failed_login_attempts=5,
            locked_until=datetime.now(),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.failed_login_attempts == 5
        assert user.locked_until is not None

    finally:
        db.query(User).filter(
            User.username == "locked_test_user"
        ).delete()
        db.commit()
        db.close()
