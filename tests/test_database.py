from sqlalchemy import text
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from dependencies.database import get_db


def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1


def test_session_local():
    db = SessionLocal()

    try:
        assert isinstance(db, Session)

        result = db.execute(text("SELECT 1"))

        assert result.scalar() == 1

    finally:
        db.close()


def test_get_db_dependency():
    db_generator = get_db()

    db = next(db_generator)

    try:
        assert isinstance(db, Session)

    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass
