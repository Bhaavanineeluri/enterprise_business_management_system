from fastapi import APIRouter, HTTPException, Query, Response, status

from schemas.employees.employee import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeePatch,
    EmployeeResponse,
    EmployeeSingleResponse,
    EmployeeUpdate,
)
from services.employees.employee_service import (
    create_employee,
    delete_employee,
    get_employee,
    get_employees,
    patch_employee,
    update_employee,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post(
    "",
    response_model=EmployeeSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_api(
    employee_data: EmployeeCreate,
    response: Response,
):
    employee = create_employee(employee_data)

    response.headers["Location"] = f"/api/v1/employees/{employee['id']}"

    return {
        "success": True,
        "message": "Employee created successfully",
        "data": employee,
    }


@router.get(
    "",
    response_model=EmployeeListResponse,
    status_code=status.HTTP_200_OK,
)
def get_employees_api(
    department: str | None = Query(
        default=None,
        description="Filter employees by department",
    ),
    name: str | None = Query(
        default=None,
        description="Search employees by name",
    ),
    active: bool | None = Query(
        default=None,
        description="Filter employees by active status",
    ),
):
    employees = get_employees(
        department=department,
        name=name,
        active=active,
    )

    return {
        "success": True,
        "message": "Employees retrieved successfully",
        "data": employees,
    }


@router.get(
    "/{employee_id}",
    response_model=EmployeeSingleResponse,
    status_code=status.HTTP_200_OK,
)
def get_employee_api(employee_id: int):

    employee = get_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return {
        "success": True,
        "message": "Employee retrieved successfully",
        "data": employee,
    }


@router.put(
    "/{employee_id}",
    response_model=EmployeeSingleResponse,
    status_code=status.HTTP_200_OK,
)
def update_employee_api(
    employee_id: int,
    employee_data: EmployeeUpdate,
):

    employee = update_employee(
        employee_id,
        employee_data,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return {
        "success": True,
        "message": "Employee updated successfully",
        "data": employee,
    }


@router.patch(
    "/{employee_id}",
    response_model=EmployeeSingleResponse,
    status_code=status.HTTP_200_OK,
)
def patch_employee_api(
    employee_id: int,
    employee_data: EmployeePatch,
):

    employee = patch_employee(
        employee_id,
        employee_data,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return {
        "success": True,
        "message": "Employee partially updated successfully",
        "data": employee,
    }


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_employee_api(employee_id: int):

    deleted = delete_employee(employee_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
