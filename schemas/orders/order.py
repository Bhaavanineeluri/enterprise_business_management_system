from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderCreate(BaseModel):
    order_code: str = Field(..., min_length=2, max_length=50)
    customer_id: int = Field(..., gt=0)
    status: str = Field(default="pending", min_length=2, max_length=30)
    total_amount: Decimal = Field(default=Decimal("0.00"), ge=0)

    @field_validator("order_code", "status", mode="before")
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip().lower() if value != "pending" else value.strip()
        return value


class OrderUpdate(BaseModel):
    customer_id: int | None = Field(default=None, gt=0)
    status: str | None = Field(default=None, min_length=2, max_length=30)
    total_amount: Decimal | None = Field(default=None, ge=0)

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value


class OrderPatch(OrderUpdate):
    pass


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_code: str
    customer_id: int
    status: str
    total_amount: Decimal
    order_date: datetime
    created_at: datetime
    updated_at: datetime


class OrderSingleResponse(BaseModel):
    success: bool
    message: str
    data: OrderResponse


class OrderListData(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    page_size: int
    pages: int


class OrderListResponse(BaseModel):
    success: bool
    message: str
    data: OrderListData
