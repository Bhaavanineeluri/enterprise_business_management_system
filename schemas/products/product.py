from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    product_code: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=150)
    category: str | None = Field(default=None, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    price: float = Field(..., gt=0)
    cost_price: float | None = Field(default=None, gt=0)
    stock: int = Field(default=0, ge=0)
    minimum_stock: int = Field(default=10, ge=0)
    vendor_id: int | None = Field(default=None, gt=0)

    @field_validator(
        "product_code",
        "name",
        "category",
        "brand",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class ProductUpdate(BaseModel):
    product_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    category: str | None = Field(default=None, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    price: float | None = Field(default=None, gt=0)
    cost_price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    minimum_stock: int | None = Field(default=None, ge=0)
    vendor_id: int | None = Field(default=None, gt=0)

    @field_validator(
        "product_code",
        "name",
        "category",
        "brand",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class ProductPatch(ProductUpdate):
    pass


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_code: str
    name: str
    category: str | None
    brand: str | None
    price: float
    cost_price: float | None
    stock: int
    minimum_stock: int
    vendor_id: int | None
    created_at: datetime
    updated_at: datetime


class ProductSingleResponse(BaseModel):
    success: bool
    message: str
    data: ProductResponse


class ProductListData(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
    pages: int


class ProductListResponse(BaseModel):
    success: bool
    message: str
    data: ProductListData
