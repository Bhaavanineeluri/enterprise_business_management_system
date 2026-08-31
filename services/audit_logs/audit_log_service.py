import json

from sqlalchemy.orm import Session

from models.audit_logs.audit_log import AuditLog


def create_audit_log(
    db: Session,
    action: str,
    user_id: int | None = None,
    resource: str | None = None,
    resource_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    details: dict | None = None,
) -> AuditLog:

    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=json.dumps(details) if details else None,
    )

    try:
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
    except Exception:
        db.rollback()
        raise

    return audit_log
