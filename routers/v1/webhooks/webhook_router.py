from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.webhooks.webhook import Webhook
from schemas.webhooks.webhook import WebhookCreate, WebhookResponse
from services.webhooks.webhook_service import (
    create_webhook,
    deliver_webhook,
    retry_webhook,
)

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post(
    "/",
    response_model=WebhookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_webhook_api(
    webhook_data: WebhookCreate,
    db: Session = Depends(get_db),
):
    return create_webhook(db, webhook_data)


@router.post(
    "/{webhook_id}/deliver",
    response_model=WebhookResponse,
)
def deliver_webhook_api(
    webhook_id: int,
    db: Session = Depends(get_db),
):
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id
    ).first()

    if webhook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    return deliver_webhook(db, webhook)


@router.post(
    "/{webhook_id}/retry",
    response_model=WebhookResponse,
)
def retry_webhook_api(
    webhook_id: int,
    db: Session = Depends(get_db),
):
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id
    ).first()

    if webhook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    return retry_webhook(db, webhook)
