from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from models.employees.employee import Employee


def create(
    db: Session,
    employee: Employee,
) -> Employee:

    db.add(employee)
    db.flush()

    return employee


def get_all(
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

    query = db.query(Employee).filter(
        Employee.deleted_at.is_(None)
    )

    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    if name is not None:
        query = query.filter(
            Employee.full_name.ilike(f"%{name}%")
        )

    if email is not None:
        query = query.filter(
            Employee.email.ilike(f"%{email}%")
        )

    if employee_code is not None:
        query = query.filter(
            Employee.employee_code.ilike(
                f"%{employee_code}%"
            )
        )

    sort_columns = {
        "id": Employee.id,
        "employee_code": Employee.employee_code,
        "full_name": Employee.full_name,
        "email": Employee.email,
        "department_id": Employee.department_id,
        "created_at": Employee.created_at,
        "updated_at": Employee.updated_at,
    }

    sort_column = sort_columns.get(sort_by, Employee.id)

    if sort_order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    total = query.count()

    employees = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return employees, total


def get_by_id(
    db: Session,
    employee_id: int,
) -> Employee | None:

    return (
        db.query(Employee)
        .filter(
            Employee.id == employee_id,
            Employee.deleted_at.is_(None),
        )
        .first()
    )


def update(
    db: Session,
    employee: Employee,
    update_data: dict,
) -> Employee:

    for field, value in update_data.items():
        setattr(employee, field, value)

    db.flush()

    return employee


def delete(
    db: Session,
    employee: Employee,
) -> None:

    db.delete(employee)
    db.flush()