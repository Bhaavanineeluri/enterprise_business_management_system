from pydantic import BaseModel, EmailStr, Field, field_validator

from security.password_policy import validate_password_policy


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    success: bool
    message: str
    reset_token: str


class ResetPasswordRequest(BaseModel):
    token: str = Field(
        ...,
        min_length=6,
        max_length=255,
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        return validate_password_policy(value)


class ResetPasswordResponse(BaseModel):
    success: bool
    message: str
