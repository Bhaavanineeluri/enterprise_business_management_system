from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WebhookCreate(BaseModel):
    event_type: str
    target_url: str
    payload: dict


class WebhookResponse(BaseModel):
    id: int
    event_type: str
    target_url: str
    payload: dict
    status: str
    attempts: int
    created_at: datetime
    delivered_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
