from pydantic import BaseModel, Field

from schemas.employees.employee import (
    EmployeeCreate,
    EmployeeUpdate,
)


class BulkEmployeeCreate(BaseModel):
    employees: list[EmployeeCreate] = Field(
        ...,
        min_length=1,
        max_length=100,
    )


class BulkEmployeeUpdateItem(BaseModel):
    employee_id: int = Field(
        ...,
        gt=0,
    )

    data: EmployeeUpdate


class BulkEmployeeUpdate(BaseModel):
    employees: list[BulkEmployeeUpdateItem] = Field(
        ...,
        min_length=1,
        max_length=100,
    )


class BulkEmployeeDelete(BaseModel):
    employee_ids: list[int] = Field(
        ...,
        min_length=1,
        max_length=100,
    )
