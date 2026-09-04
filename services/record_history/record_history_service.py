from sqlalchemy.orm import Session

from models.record_history.record_history import RecordHistory


def create_record_history(
    db: Session,
    user_id: int | None,
    resource: str,
    resource_id: int | str,
    field_name: str,
    old_value: str | None,
    new_value: str | None,
) -> RecordHistory:
    history = RecordHistory(
        user_id=user_id,
        resource=resource,
        resource_id=str(resource_id),
        field_name=field_name,
        old_value=old_value,
        new_value=new_value,
    )

    db.add(history)
    db.flush()

    return history


def get_record_history(
    db: Session,
    resource: str,
    resource_id: int | str,
) -> list[RecordHistory]:
    return (
        db.query(RecordHistory)
        .filter(
            RecordHistory.resource == resource,
            RecordHistory.resource_id == str(resource_id),
        )
        .order_by(RecordHistory.changed_at.desc())
        .all()
    )


def get_resource_history(
    db: Session,
    resource: str,
) -> list[RecordHistory]:
    return (
        db.query(RecordHistory)
        .filter(RecordHistory.resource == resource)
        .order_by(RecordHistory.changed_at.desc())
        .all()
    )
