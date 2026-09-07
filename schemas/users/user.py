from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from security.password_policy import validate_password_policy


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        if not isinstance(value, str):
            return value

        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_policy(value)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime


class UserRegistrationResponse(BaseModel):
    success: bool
    message: str
    data: UserResponse
    
    
class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    success: bool
    message: str
    data: UserResponse
    access_token: str
    token_type: str = "bearer"
    