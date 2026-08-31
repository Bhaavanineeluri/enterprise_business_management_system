from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    device_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    device_name: str | None = Field(
        default=None,
        max_length=255,
    )

    device_type: str | None = Field(
        default=None,
        max_length=50,
    )


class DeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    device_id: str
    device_name: str | None
    device_type: str | None
    ip_address: str | None
    user_agent: str | None
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime
