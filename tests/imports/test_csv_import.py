import pytest

from schemas.employees.employee import EmployeeCreate
from schemas.imports.csv_import import CSVImportResponse


def test_csv_import_response_schema():
    response = CSVImportResponse(
        success=True,
        message="CSV import completed",
        total_rows=3,
        imported_rows=2,
        failed_rows=1,
        errors=["Row 3: invalid email"],
    )

    assert response.success is True
    assert response.total_rows == 3
    assert response.imported_rows == 2
    assert response.failed_rows == 1
    assert len(response.errors) == 1


def test_employee_csv_data_uses_employee_validation():
    employee = EmployeeCreate(
        employee_code="EMP100",
        full_name="Test Employee",
        email="test.employee@example.com",
        department_id=1,
    )

    assert employee.employee_code == "EMP100"
    assert employee.full_name == "Test Employee"
    assert employee.email == "test.employee@example.com"
    assert employee.department_id == 1


def test_invalid_employee_email():
    with pytest.raises(ValueError):
        EmployeeCreate(
            employee_code="EMP101",
            full_name="Test Employee",
            email="invalid-email",
            department_id=1,
        )


def test_invalid_department_id():
    with pytest.raises(ValueError):
        EmployeeCreate(
            employee_code="EMP102",
            full_name="Test Employee",
            email="test@example.com",
            department_id=0,
        )
