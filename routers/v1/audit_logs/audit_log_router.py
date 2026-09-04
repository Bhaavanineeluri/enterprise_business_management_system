from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from models.audit_logs.audit_log import AuditLog
from schemas.audit_logs.audit_log import AuditLogResponse
from services.audit_logs.audit_log_service import create_audit_log


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.post(
    "/",
    response_model=AuditLogResponse,
    status_code=status.HTTP_200_OK,
)
def create_audit_log_endpoint(
    action: str,
    user_id: int | None = None,
    resource: str | None = None,
    resource_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    details: str | None = None,
    db: Session = Depends(get_db),
):
    parsed_details = None

    if details:
        import json

        try:
            parsed_details = json.loads(details)
        except json.JSONDecodeError:
            parsed_details = {
                "raw": details,
            }

    return create_audit_log(
        db=db,
        action=action,
        user_id=user_id,
        resource=resource,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=parsed_details,
    )


@router.get(
    "/",
    response_model=list[AuditLogResponse],
)
def get_audit_logs(
    action: str | None = Query(
        default=None,
        description="Filter by audit action",
    ),
    user_id: int | None = Query(
        default=None,
        gt=0,
        description="Filter by user ID",
    ),
    resource: str | None = Query(
        default=None,
        description="Filter by resource",
    ),
    db: Session = Depends(get_db),
):
    query = db.query(AuditLog)

    if action is not None:
        query = query.filter(
            AuditLog.action == action
        )

    if user_id is not None:
        query = query.filter(
            AuditLog.user_id == user_id
        )

    if resource is not None:
        query = query.filter(
            AuditLog.resource == resource
        )

    return (
        query
        .order_by(AuditLog.created_at.desc())
        .all()
    )


@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse,
)
def get_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
):
    audit_log = (
        db.query(AuditLog)
        .filter(AuditLog.id == audit_log_id)
        .first()
    )

    if audit_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found",
        )

    return audit_log