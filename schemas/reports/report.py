from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReportCreate(BaseModel):
    report_code: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=150)
    report_type: str = Field(..., min_length=2, max_length=50)
    description: str | None = None
    status: str = Field(default="pending", min_length=2, max_length=30)
    generated_file: str | None = Field(default=None, max_length=255)
    generated_at: datetime | None = None

    @field_validator(
        "report_code",
        "name",
        "report_type",
        "description",
        "status",
        "generated_file",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class ReportUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    report_type: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = None
    status: str | None = Field(default=None, min_length=2, max_length=30)
    generated_file: str | None = Field(default=None, max_length=255)
    generated_at: datetime | None = None

    @field_validator(
        "name",
        "report_type",
        "description",
        "status",
        "generated_file",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class ReportPatch(ReportUpdate):
    pass


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    report_code: str
    name: str
    report_type: str
    description: str | None
    status: str
    generated_file: str | None
    generated_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ReportSingleResponse(BaseModel):
    success: bool
    message: str
    data: ReportResponse


class ReportListData(BaseModel):
    items: list[ReportResponse]
    total: int
    page: int
    page_size: int
    pages: int


class ReportListResponse(BaseModel):
    success: bool
    message: str
    data: ReportListData
