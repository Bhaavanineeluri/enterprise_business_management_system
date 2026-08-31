from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    action: str
    resource: str | None
    resource_id: str | None
    ip_address: str | None
    user_agent: str | None
    details: str | None
    created_at: datetime
