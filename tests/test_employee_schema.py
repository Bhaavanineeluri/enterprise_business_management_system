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
        department_id=1,
    )

    assert employee.employee_code == "EMP001"
    assert employee.full_name == "John Smith"
    assert employee.department_id == 1


def test_strings_are_normalized():
    employee = EmployeeCreate(
        employee_code="  EMP001  ",
        full_name="  John Smith  ",
        email="john@example.com",
        department_id=1,
    )

    assert employee.employee_code == "EMP001"
    assert employee.full_name == "John Smith"


def test_invalid_email():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="EMP001",
            full_name="John Smith",
            email="invalid-email",
            department_id=1,
        )


def test_employee_code_too_short():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="E",
            full_name="John Smith",
            email="john@example.com",
            department_id=1,
        )


def test_full_name_too_short():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="EMP001",
            full_name="J",
            email="john@example.com",
            department_id=1,
        )


def test_full_name_must_contain_letter():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="EMP001",
            full_name="123456",
            email="john@example.com",
            department_id=1,
        )


def test_department_id_must_be_positive():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_code="EMP001",
            full_name="John Smith",
            email="john@example.com",
            department_id=0,
        )


def test_patch_allows_partial_update():
    employee = EmployeePatch(
        department_id=2,
    )

    assert employee.department_id == 2
    assert employee.employee_code is None
    assert employee.full_name is None
    assert employee.email is None