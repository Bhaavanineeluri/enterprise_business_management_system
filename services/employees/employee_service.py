from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.employees.employee import Employee
from repositories.employees import employee_repository
from schemas.employees.employee import (
    EmployeeCreate,
    EmployeePatch,
    EmployeeUpdate,
)
from schemas.employees.bulk import BulkEmployeeUpdateItem
from services.record_history.record_history_service import create_record_history
from services.redis.redis_service import (
    get_cached_data,
    invalidate_employee_cache,
    set_cached_data,
)


def create_employee(
    db: Session,
    employee_data: EmployeeCreate,
) -> Employee:

    employee = Employee(
        employee_code=employee_data.employee_code,
        full_name=employee_data.full_name,
        email=str(employee_data.email),
        department_id=employee_data.department_id,
    )

    try:
        employee_repository.create(db, employee)
        db.commit()
        db.refresh(employee)
    except Exception:
        db.rollback()
        raise

    return employee


def get_employees(
    db: Session,
    department_id: int | None = None,
    name: str | None = None,
    email: str | None = None,
    employee_code: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    offset: int = 0,
    limit: int = 10,
) -> tuple[list[Employee], int]:

    return employee_repository.get_all(
        db,
        department_id=department_id,
        name=name,
        email=email,
        employee_code=employee_code,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )


def get_employee(
    db: Session,
    employee_id: int,
) -> Employee | None:

    cache_key = f"employee:{employee_id}"

    cached_employee = get_cached_data(cache_key)

    if cached_employee is not None:
        return cached_employee

    employee = employee_repository.get_by_id(
        db,
        employee_id,
    )

    if employee is None:
        return None

    employee_data = {
        "id": employee.id,
        "employee_code": employee.employee_code,
        "full_name": employee.full_name,
        "email": employee.email,
        "department_id": employee.department_id,
        "deleted_at": employee.deleted_at.isoformat()
        if employee.deleted_at
        else None,
    }

    set_cached_data(
        cache_key,
        employee_data,
        expiration=300,
    )

    return employee


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate,
    user_id: int | None = None,
) -> Employee | None:

    employee = employee_repository.get_by_id(
        db,
        employee_id,
    )

    if employee is None:
        return None

    update_data = employee_data.model_dump(
        exclude_unset=True,
    )

    history_entries = []

    for field_name, new_value in update_data.items():
        old_value = getattr(employee, field_name, None)

        if old_value != new_value:
            history_entries.append(
                {
                    "field_name": field_name,
                    "old_value": None if old_value is None else str(old_value),
                    "new_value": None if new_value is None else str(new_value),
                }
            )

    try:
        employee_repository.update(
            db,
            employee,
            update_data,
        )

        for entry in history_entries:
            create_record_history(
                db=db,
                user_id=user_id,
                resource="employees",
                resource_id=employee.id,
                field_name=entry["field_name"],
                old_value=entry["old_value"],
                new_value=entry["new_value"],
            )

        db.commit()
        db.refresh(employee)
        invalidate_employee_cache(employee_id)

    except Exception:
        db.rollback()
        raise

    return employee


def patch_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeePatch,
) -> Employee | None:

    employee = employee_repository.get_by_id(
        db,
        employee_id,
    )

    if employee is None:
        return None

    update_data = employee_data.model_dump(
        exclude_unset=True,
    )

    try:
        employee_repository.update(
            db,
            employee,
            update_data,
        )
        db.commit()
        db.refresh(employee)
        invalidate_employee_cache(employee_id)
    except Exception:
        db.rollback()
        raise

    return employee


def delete_employee(
    db: Session,
    employee_id: int,
) -> bool:

    employee = employee_repository.get_by_id(
        db,
        employee_id,
    )

    if employee is None:
        return False

    try:
        employee.deleted_at = datetime.now(timezone.utc)
        db.commit()
        invalidate_employee_cache(employee_id)
    except Exception:
        db.rollback()
        raise

    return True


def restore_employee(
    db: Session,
    employee_id: int,
) -> Employee | None:

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == employee_id,
            Employee.deleted_at.is_not(None),
        )
        .first()
    )

    if employee is None:
        return None

    try:
        employee.deleted_at = None
        db.commit()
        db.refresh(employee)
        invalidate_employee_cache(employee_id)
    except Exception:
        db.rollback()
        raise

    return employee


def bulk_create_employees(
    db: Session,
    employees_data: list[EmployeeCreate],
) -> list[Employee]:

    employees = [
        Employee(
            employee_code=employee_data.employee_code,
            full_name=employee_data.full_name,
            email=str(employee_data.email),
            department_id=employee_data.department_id,
        )
        for employee_data in employees_data
    ]

    try:
        db.add_all(employees)
        db.commit()

        for employee in employees:
            db.refresh(employee)

    except Exception:
        db.rollback()
        raise

    return employees


def bulk_update_employees(
    db: Session,
    employees_data: list[BulkEmployeeUpdateItem],
) -> list[Employee]:

    updated_employees: list[Employee] = []

    try:
        for item in employees_data:

            employee = (
                db.query(Employee)
                .filter(
                    Employee.id == item.employee_id,
                    Employee.deleted_at.is_(None),
                )
                .first()
            )

            if employee is None:
                raise ValueError(
                    f"Employee with id {item.employee_id} not found"
                )

            update_data = item.data.model_dump(
                exclude_unset=True,
            )

            for field, value in update_data.items():
                if field == "email":
                    value = str(value)

                setattr(
                    employee,
                    field,
                    value,
                )

            updated_employees.append(employee)

        db.commit()

        for employee in updated_employees:
            db.refresh(employee)

    except Exception:
        db.rollback()
        raise

    return updated_employees


def bulk_delete_employees(
    db: Session,
    employee_ids: list[int],
) -> int:

    deleted_count = 0

    try:
        for employee_id in employee_ids:

            employee = (
                db.query(Employee)
                .filter(
                    Employee.id == employee_id,
                    Employee.deleted_at.is_(None),
                )
                .first()
            )

            if employee is None:
                raise ValueError(
                    f"Employee with id {employee_id} not found"
                )

            employee.deleted_at = datetime.now(
                timezone.utc
            ).replace(tzinfo=None)

            deleted_count += 1

        db.commit()

    except Exception:
        db.rollback()
        raise

    return deleted_count
