import csv
import io

from sqlalchemy.orm import Session
from pydantic import ValidationError

from models.employees.employee import Employee
from models.departments.department import Department
from schemas.employees.employee import EmployeeCreate


REQUIRED_COLUMNS = {
    "employee_code",
    "full_name",
    "email",
    "department_id",
}


def import_employees_from_csv(
    db: Session,
    csv_content: bytes,
) -> dict:

    total_rows = 0
    imported_rows = 0
    failed_rows = 0
    errors: list[str] = []

    try:
        text = csv_content.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError(
            "CSV file must use UTF-8 encoding"
        )

    reader = csv.DictReader(
        io.StringIO(text)
    )

    if reader.fieldnames is None:
        raise ValueError(
            "CSV file must contain a header row"
        )

    columns = {
        column.strip()
        for column in reader.fieldnames
        if column
    }

    missing_columns = REQUIRED_COLUMNS - columns

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    employees: list[Employee] = []

    for row_number, row in enumerate(
        reader,
        start=2,
    ):
        total_rows += 1

        try:
            employee_data = EmployeeCreate(
                employee_code=row.get(
                    "employee_code",
                    "",
                ),
                full_name=row.get(
                    "full_name",
                    "",
                ),
                email=row.get(
                    "email",
                    "",
                ),
                department_id=int(
                    row.get(
                        "department_id",
                        0,
                    )
                ),
            )

            department = (
                db.query(Department)
                .filter(
                    Department.id
                    == employee_data.department_id
                )
                .first()
            )

            if department is None:
                raise ValueError(
                    f"Department {employee_data.department_id} not found"
                )

            existing_employee = (
                db.query(Employee)
                .filter(
                    (
                        Employee.employee_code
                        == employee_data.employee_code
                    )
                    | (
                        Employee.email
                        == str(employee_data.email)
                    )
                )
                .first()
            )

            if existing_employee is not None:
                raise ValueError(
                    "Employee code or email already exists"
                )

            employees.append(
                Employee(
                    employee_code=employee_data.employee_code,
                    full_name=employee_data.full_name,
                    email=str(employee_data.email),
                    department_id=employee_data.department_id,
                )
            )

            imported_rows += 1

        except (ValueError, ValidationError) as exc:
            failed_rows += 1

            errors.append(
                f"Row {row_number}: {exc}"
            )

    if employees:
        try:
            db.add_all(employees)
            db.commit()

        except Exception:
            db.rollback()
            raise

    return {
        "total_rows": total_rows,
        "imported_rows": imported_rows,
        "failed_rows": failed_rows,
        "errors": errors,
    }
