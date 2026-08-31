from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.sessions.session import UserSession


def create_session(
    db: Session,
    user_id: int,
    session_token: str,
    expires_at: datetime,
) -> UserSession:

    session = UserSession(
        user_id=user_id,
        session_token=session_token,
        expires_at=expires_at,
        is_active=True,
    )

    try:
        db.add(session)
        db.commit()
        db.refresh(session)

    except Exception:
        db.rollback()
        raise

    return session


def revoke_session(
    db: Session,
    session_token: str,
) -> bool:

    session = (
        db.query(UserSession)
        .filter(
            UserSession.session_token == session_token,
            UserSession.is_active.is_(True),
        )
        .first()
    )

    if session is None:
        return False

    session.is_active = False
    session.revoked_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.commit()

    return True


def revoke_all_sessions(
    db: Session,
    user_id: int,
) -> int:

    sessions = (
        db.query(UserSession)
        .filter(
            UserSession.user_id == user_id,
            UserSession.is_active.is_(True),
        )
        .all()
    )

    now = datetime.now()

    for session in sessions:
        session.is_active = False
        session.revoked_at = now

    db.commit()

    return len(sessions)