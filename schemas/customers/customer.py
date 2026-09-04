from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerCreate(BaseModel):
    customer_code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    company_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    contact_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    @field_validator(
        "customer_code",
        "company_name",
        "contact_name",
        "phone",
        "address",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class CustomerUpdate(BaseModel):
    customer_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    company_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    contact_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    @field_validator(
        "customer_code",
        "company_name",
        "contact_name",
        "phone",
        "address",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class CustomerPatch(CustomerUpdate):
    pass


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_code: str
    company_name: str
    contact_name: str
    email: EmailStr
    phone: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime


class CustomerSingleResponse(BaseModel):
    success: bool
    message: str
    data: CustomerResponse


class CustomerListData(BaseModel):
    items: list[CustomerResponse]
    total: int
    page: int
    page_size: int
    pages: int


class CustomerListResponse(BaseModel):
    success: bool
    message: str
    data: CustomerListData
