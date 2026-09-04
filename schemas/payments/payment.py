from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PaymentCreate(BaseModel):
    payment_code: str = Field(..., min_length=2, max_length=50)
    order_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0)
    payment_method: str = Field(
        default="cash",
        min_length=2,
        max_length=30,
    )
    status: str = Field(
        default="pending",
        min_length=2,
        max_length=30,
    )
    transaction_reference: str | None = Field(
        default=None,
        max_length=100,
    )

    @field_validator(
        "payment_code",
        "payment_method",
        "status",
        "transaction_reference",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value


class PaymentUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0)
    payment_method: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    status: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    transaction_reference: str | None = Field(
        default=None,
        max_length=100,
    )

    @field_validator(
        "payment_method",
        "status",
        "transaction_reference",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value


class PaymentPatch(PaymentUpdate):
    pass


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    payment_code: str
    order_id: int
    amount: Decimal
    payment_method: str
    status: str
    transaction_reference: str | None
    payment_date: datetime
    created_at: datetime
    updated_at: datetime


class PaymentSingleResponse(BaseModel):
    success: bool
    message: str
    data: PaymentResponse


class PaymentListData(BaseModel):
    items: list[PaymentResponse]
    total: int
    page: int
    page_size: int
    pages: int


class PaymentListResponse(BaseModel):
    success: bool
    message: str
    data: PaymentListData
