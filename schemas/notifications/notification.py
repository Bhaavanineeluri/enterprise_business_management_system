from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    user_id: int = Field(
        ...,
        gt=0,
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class NotificationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime
    read_at: datetime | None


class NotificationMessageResponse(BaseModel):
    success: bool
    message: str
    data: NotificationResponse


class NotificationListData(BaseModel):
    items: list[NotificationResponse]
    total: int


class NotificationListResponse(BaseModel):
    success: bool
    message: str
    data: NotificationListData
