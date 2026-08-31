from pydantic import BaseModel, EmailStr, Field


class BackgroundEmailRequest(BaseModel):
    recipient: EmailStr
    subject: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class BackgroundNotificationRequest(BaseModel):
    user_id: int = Field(
        ...,
        gt=0,
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class BackgroundTaskResponse(BaseModel):
    success: bool
    message: str
