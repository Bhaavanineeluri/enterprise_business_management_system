from datetime import datetime

from sqlalchemy.orm import Session

from database import SessionLocal
from models.password_resets.password_reset import PasswordReset


def cleanup_password_reset_tokens() -> None:
    db: Session = SessionLocal()

    try:
        deleted_count = (
            db.query(PasswordReset)
            .filter(
                PasswordReset.expires_at < datetime.now()
            )
            .delete(
                synchronize_session=False
            )
        )

        db.commit()

        print(
            f"[SCHEDULED JOB] "
            f"Deleted {deleted_count} expired password reset tokens"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
