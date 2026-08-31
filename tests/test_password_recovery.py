from datetime import datetime, timedelta
import hashlib
import secrets

from database import SessionLocal
from models.password_resets.password_reset import PasswordReset
from models.users.user import User
from security.password import hash_password, verify_password
from services.password_resets.password_reset_service import (
    create_password_reset_token,
    reset_password,
)


def cleanup_user(db, username):
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if user is not None:
        db.query(PasswordReset).filter(
            PasswordReset.user_id == user.id
        ).delete(
            synchronize_session=False
        )

        db.delete(user)
        db.commit()


def test_create_password_reset_token():
    db = SessionLocal()

    username = "password_reset_test_user"

    try:
        cleanup_user(db, username)

        user = User(
            username=username,
            email="password_reset_test@example.com",
            hashed_password=hash_password("OldPass123"),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_password_reset_token(
            db,
            user.email,
        )

        assert token is not None
        assert len(token) > 20

        reset = (
            db.query(PasswordReset)
            .filter(
                PasswordReset.user_id == user.id
            )
            .first()
        )

        assert reset is not None
        assert reset.used is False
        assert reset.expires_at > datetime.now()

    finally:
        cleanup_user(db, username)
        db.close()


def test_reset_password():
    db = SessionLocal()

    username = "reset_password_test_user"

    try:
        cleanup_user(db, username)

        user = User(
            username=username,
            email="reset_password_test@example.com",
            hashed_password=hash_password("OldPass123"),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_password_reset_token(
            db,
            user.email,
        )

        reset_password(
            db,
            token,
            "NewPass123",
        )

        db.refresh(user)

        assert verify_password(
            "NewPass123",
            user.hashed_password,
        )

        assert not verify_password(
            "OldPass123",
            user.hashed_password,
        )

        reset = (
            db.query(PasswordReset)
            .filter(
                PasswordReset.user_id == user.id
            )
            .first()
        )

        assert reset.used is True

    finally:
        cleanup_user(db, username)
        db.close()


def test_expired_reset_token():
    db = SessionLocal()

    username = "expired_reset_test_user"

    try:
        cleanup_user(db, username)

        user = User(
            username=username,
            email="expired_reset_test@example.com",
            hashed_password=hash_password("OldPass123"),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

        reset = PasswordReset(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now() - timedelta(minutes=1),
            used=False,
        )

        db.add(reset)
        db.commit()

        try:
            reset_password(
                db,
                token,
                "NewPass123",
            )

            assert False, "Expected expired token to fail"

        except Exception as exc:
            assert "expired" in str(exc).lower()

    finally:
        cleanup_user(db, username)
        db.close()




def test_invalid_reset_token():
    db = SessionLocal()

    try:
        try:
            reset_password(
                db,
                "invalid-token-123456789",
                "NewPass123",
            )

            assert False, "Expected invalid token to fail"

        except Exception as exc:
            assert "invalid" in str(exc).lower()

    finally:
        db.close()


def test_already_used_reset_token():
    db = SessionLocal()

    username = "used_reset_test_user"

    try:
        cleanup_user(db, username)

        user = User(
            username=username,
            email="used_reset_test@example.com",
            hashed_password=hash_password("OldPass123"),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_password_reset_token(
            db,
            user.email,
        )

        reset_password(
            db,
            token,
            "NewPass123",
        )

        try:
            reset_password(
                db,
                token,
                "AnotherPass123",
            )

            assert False, "Expected used token to fail"

        except Exception as exc:
            assert "used" in str(exc).lower()

    finally:
        cleanup_user(db, username)
        db.close()
