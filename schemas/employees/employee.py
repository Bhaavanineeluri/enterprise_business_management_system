from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from schemas.common.response import APIResponse


class EmployeeCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    department: str = Field(
        min_length=2,
        max_length=50,
    )

    active: bool = True

    @field_validator("name", "department")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not any(character.isalpha() for character in value):
            raise ValueError("Name must contain at least one letter")

        return value

    @model_validator(mode="after")
    def validate_employee(self) -> Self:
        if self.active and self.department.lower() == "terminated":
            raise ValueError(
                "An employee in the terminated department cannot be active"
            )

        return self


class EmployeeUpdate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    department: str = Field(
        min_length=2,
        max_length=50,
    )

    active: bool

    @field_validator("name", "department")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not any(character.isalpha() for character in value):
            raise ValueError("Name must contain at least one letter")

        return value

    @model_validator(mode="after")
    def validate_employee(self) -> Self:
        if self.active and self.department.lower() == "terminated":
            raise ValueError(
                "An employee in the terminated department cannot be active"
            )

        return self


class EmployeePatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: EmailStr | None = None

    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    active: bool | None = None

    @field_validator("name", "department")
    @classmethod
    def normalize_text(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        if not any(character.isalpha() for character in value):
            raise ValueError("Name must contain at least one letter")

        return value


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    department: str
    active: bool


class EmployeeListResponse(APIResponse[list[EmployeeResponse]]):
    pass


class EmployeeSingleResponse(APIResponse[EmployeeResponse]):
    pass
