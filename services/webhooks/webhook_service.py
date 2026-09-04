import json
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from models.webhooks.webhook import Webhook
from schemas.webhooks.webhook import WebhookCreate


def webhook_to_dict(webhook: Webhook) -> dict:
    return {
        "id": webhook.id,
        "event_type": webhook.event_type,
        "target_url": webhook.target_url,
        "payload": json.loads(webhook.payload),
        "status": webhook.status,
        "attempts": webhook.attempts,
        "created_at": webhook.created_at,
        "delivered_at": webhook.delivered_at,
    }


def create_webhook(
    db: Session,
    webhook_data: WebhookCreate,
) -> dict:

    webhook = Webhook(
        event_type=webhook_data.event_type,
        target_url=webhook_data.target_url,
        payload=json.dumps(webhook_data.payload),
        status="pending",
        attempts=0,
    )

    db.add(webhook)
    db.commit()
    db.refresh(webhook)

    return webhook_to_dict(webhook)


def deliver_webhook(
    db: Session,
    webhook: Webhook,
) -> dict:

    webhook.attempts += 1

    try:
        payload = json.loads(webhook.payload)

        response = httpx.post(
            webhook.target_url,
            json=payload,
            timeout=10,
        )

        if 200 <= response.status_code < 300:
            webhook.status = "delivered"
            webhook.delivered_at = datetime.now(timezone.utc)

        else:
            webhook.status = "failed"

    except Exception:
        webhook.status = "failed"

    db.commit()
    db.refresh(webhook)

    return webhook_to_dict(webhook)


def retry_webhook(
    db: Session,
    webhook: Webhook,
    max_attempts: int = 3,
) -> dict:

    if webhook.status == "delivered":
        return webhook_to_dict(webhook)

    if webhook.attempts >= max_attempts:
        webhook.status = "failed"
        db.commit()
        db.refresh(webhook)
        return webhook_to_dict(webhook)

    return deliver_webhook(db, webhook)
