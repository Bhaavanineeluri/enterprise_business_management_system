import csv
import io

from sqlalchemy.orm import Session

from models.employees.employee import Employee


EXPORT_COLUMNS = [
    "employee_code",
    "full_name",
    "email",
    "department_id",
]


def export_employees_to_csv(
    db: Session,
) -> str:

    employees = (
        db.query(Employee)
        .filter(
            Employee.deleted_at.is_(None)
        )
        .order_by(Employee.id)
        .all()
    )

    output = io.StringIO(
        newline=""
    )

    writer = csv.DictWriter(
        output,
        fieldnames=EXPORT_COLUMNS,
    )

    writer.writeheader()

    for employee in employees:
        writer.writerow(
            {
                "employee_code": employee.employee_code,
                "full_name": employee.full_name,
                "email": employee.email,
                "department_id": employee.department_id,
            }
        )

    return output.getvalue()
