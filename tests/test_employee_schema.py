import pytest
from pydantic import ValidationError

from schemas.employees.employee import (
    EmployeeCreate,
    EmployeePatch,
)


def test_valid_employee():
    employee = EmployeeCreate(
        name="John Smith",
        email="john@example.com",
        department="Engineering",
        active=True,
    )

    assert employee.name == "John Smith"
    assert employee.department == "Engineering"


def test_name_is_normalized():
    employee = EmployeeCreate(
        name="  John Smith  ",
        email="john@example.com",
        department="  Engineering  ",
    )

    assert employee.name == "John Smith"
    assert employee.department == "Engineering"


def test_invalid_email():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            name="John Smith",
            email="invalid-email",
            department="Engineering",
        )


def test_name_too_short():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            name="J",
            email="john@example.com",
            department="Engineering",
        )


def test_name_must_contain_letter():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            name="123456",
            email="john@example.com",
            department="Engineering",
        )


def test_terminated_employee_cannot_be_active():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            name="John Smith",
            email="john@example.com",
            department="terminated",
            active=True,
        )


def test_patch_allows_partial_update():
    employee = EmployeePatch(
        department="Finance",
    )

    assert employee.department == "Finance"
    assert employee.name is None
    assert employee.email is None
