from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecordHistoryResponse(BaseModel):
    id: int
    user_id: int | None
    resource: str
    resource_id: str
    field_name: str
    old_value: str | None
    new_value: str | None
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)
