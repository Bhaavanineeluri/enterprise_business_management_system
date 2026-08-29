from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    employee_code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    department: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    @field_validator(
        "employee_code",
        "full_name",
        "department",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value: str) -> str:
        if not isinstance(value, str):
            return value

        return value.strip()

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not any(char.isalpha() for char in value):
            raise ValueError(
                "full_name must contain at least one letter"
            )

        return value


class EmployeeUpdate(BaseModel):
    employee_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: EmailStr | None = None

    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    @field_validator(
        "employee_code",
        "full_name",
        "department",
        mode="before",
    )
    @classmethod
    def normalize_update_strings(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            return value

        return value.strip()


class EmployeePatch(EmployeeUpdate):
    pass


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_code: str
    full_name: str
    email: EmailStr
    department: str
    created_at: datetime
    updated_at: datetime


class EmployeeSingleResponse(BaseModel):
    employee: EmployeeResponse


class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]
    total: int