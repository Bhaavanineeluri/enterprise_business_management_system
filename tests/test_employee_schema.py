import pytest
from pydantic import ValidationError

from schemas.employees.employee import (
    EmployeeCreate,
    EmployeePatch,
)


def test_valid_employee():
    employee = EmployeeCreate(
        employee_code="EMP001",
        full_name="John Smith",
        email="john@example.com",
        department="Engineering",
    )

    assert employee.employee_code == "EMP001"
    assert employee.full_name == "John Smith"
    assert employee.department == "Engineering"


def test_strings_are_normalized():
    employee = EmployeeCreate(
        employee_code="  EMP001  ",
        full_name="  John Smith  ",
        email="john@example.com",
        department="  Engineering  ",
    )

    assert employee.employee_code == "EMP001"
    assert employee.full_name == "John Smith"
    assert employee.department == "Engineering"


def test_invalid_email():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="EMP001",
            full_name="John Smith",
            email="invalid-email",
            department="Engineering",
        )


def test_full_name_too_short():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="EMP001",
            full_name="J",
            email="john@example.com",
            department="Engineering",
        )


def test_full_name_must_contain_letter():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="EMP001",
            full_name="123456",
            email="john@example.com",
            department="Engineering",
        )


def test_patch_allows_partial_update():
    employee = EmployeePatch(
        department="Finance",
    )

    assert employee.department == "Finance"
    assert employee.employee_code is None
    assert employee.full_name is None
    assert employee.email is None
