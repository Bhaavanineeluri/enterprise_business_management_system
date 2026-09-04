from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.record_history.record_history import RecordHistoryResponse
from services.record_history.record_history_service import (
    get_record_history,
    get_resource_history,
)

router = APIRouter(
    prefix="/record-history",
    tags=["Record History"],
)


@router.get(
    "/{resource}/{resource_id}",
    response_model=list[RecordHistoryResponse],
)
def get_record_history_by_resource(
    resource: str,
    resource_id: int,
    db: Session = Depends(get_db),
):
    return get_record_history(
        db=db,
        resource=resource,
        resource_id=resource_id,
    )


@router.get(
    "/{resource}",
    response_model=list[RecordHistoryResponse],
)
def get_history_by_resource(
    resource: str,
    db: Session = Depends(get_db),
):
    return get_resource_history(
        db=db,
        resource=resource,
    )
