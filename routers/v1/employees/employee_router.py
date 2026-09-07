from dependencies.auth import get_current_user

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from dependencies.pagination import (
    PaginationParams,
    get_pagination,
)
from dependencies.database import get_db
from schemas.employees.bulk import (
    BulkEmployeeCreate,
    BulkEmployeeUpdate,
    BulkEmployeeDelete,
)
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
    restore_employee,
    update_employee,
    bulk_create_employees,
    bulk_update_employees,
    bulk_delete_employees,
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=EmployeeSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_api(
    employee_data: EmployeeCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    employee = create_employee(
        db,
        employee_data,
    )

    response.headers["Location"] = (
        f"/api/v1/employees/{employee.id}"
    )

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
    department_id: int | None = Query(
        default=None,
        description="Filter employees by department ID",
    ),
    name: str | None = Query(
        default=None,
        description="Search employees by name",
    ),
    email: str | None = Query(
        default=None,
        description="Search employees by email",
    ),

    employee_code: str | None = Query(
        default=None,
        description="Search employees by employee code",
    ),

    sort_by: str = Query(
        default="id",
        description="Sort field",
    ),

    sort_order: str = Query(
        default="asc",
        pattern="^(asc|desc)$",
        description="Sort order",
    ),
    pagination: PaginationParams = Depends(
        get_pagination
    ),
    db: Session = Depends(get_db),
):
    employees, total = get_employees(
        db,
        department_id=department_id,
        name=name,
        email=email,
        employee_code=employee_code,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.page_size,
    )

    pages = (
        (total + pagination.page_size - 1)
        // pagination.page_size
    )

    return {
        "success": True,
        "message": "Employees retrieved successfully",
        "data": {
            "items": employees,
            "total": total,
            "page": pagination.page,
            "page_size": pagination.page_size,
            "pages": pages,
        },
    }

@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
)
def bulk_create_employees_api(
    bulk_data: BulkEmployeeCreate,
    db: Session = Depends(get_db),
):
    employees = bulk_create_employees(
        db,
        bulk_data.employees,
    )

    return {
        "success": True,
        "message": "Employees created successfully",
        "data": employees,
        "total": len(employees),
    }


@router.put(
    "/bulk",
    status_code=status.HTTP_200_OK,
)
def bulk_update_employees_api(
    bulk_data: BulkEmployeeUpdate,
    db: Session = Depends(get_db),
):
    employees = bulk_update_employees(
        db,
        bulk_data.employees,
    )

    return {
        "success": True,
        "message": "Employees updated successfully",
        "data": employees,
        "total": len(employees),
    }


@router.delete(
    "/bulk",
    status_code=status.HTTP_200_OK,
)
def bulk_delete_employees_api(
    bulk_data: BulkEmployeeDelete,
    db: Session = Depends(get_db),
):
    deleted_count = bulk_delete_employees(
        db,
        bulk_data.employee_ids,
    )

    return {
        "success": True,
        "message": "Employees deleted successfully",
        "deleted_count": deleted_count,
    }

@router.get(
    "/{employee_id}",
    response_model=EmployeeSingleResponse,
    status_code=status.HTTP_200_OK,
)
def get_employee_api(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    employee = get_employee(
        db,
        employee_id,
    )

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
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    employee = update_employee(
        db,
        employee_id,
        employee_data,
        current_user.id,
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
    db: Session = Depends(get_db),
):
    employee = patch_employee(
        db,
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
def delete_employee_api(
    employee_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_employee(
        db,
        employee_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

@router.post(
    "/{employee_id}/restore",
    response_model=EmployeeSingleResponse,
    status_code=status.HTTP_200_OK,
)
def restore_employee_api(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = restore_employee(
        db,
        employee_id,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted employee not found",
        )

    return {
        "success": True,
        "message": "Employee restored successfully",
        "data": employee,
    }
