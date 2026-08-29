from schemas.employees.employee import (
    EmployeeCreate,
    EmployeePatch,
    EmployeeUpdate,
)


employees: list[dict] = []

next_employee_id = 1


def create_employee(employee_data: EmployeeCreate) -> dict:
    global next_employee_id

    employee = {
        "id": next_employee_id,
        **employee_data.model_dump(),
    }

    employees.append(employee)
    next_employee_id += 1

    return employee


def get_employees(
    department: str | None = None,
    name: str | None = None,
    active: bool | None = None,
) -> list[dict]:

    result = employees

    if department is not None:
        result = [
            employee
            for employee in result
            if employee["department"].lower() == department.lower()
        ]

    if name is not None:
        result = [
            employee
            for employee in result
            if name.lower() in employee["name"].lower()
        ]

    if active is not None:
        result = [
            employee
            for employee in result
            if employee["active"] == active
        ]

    return result


def get_employee(employee_id: int) -> dict | None:
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return None


def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> dict | None:

    employee = get_employee(employee_id)

    if employee is None:
        return None

    employee.update(employee_data.model_dump())

    return employee


def patch_employee(
    employee_id: int,
    employee_data: EmployeePatch,
) -> dict | None:

    employee = get_employee(employee_id)

    if employee is None:
        return None

    update_data = employee_data.model_dump(exclude_unset=True)

    employee.update(update_data)

    return employee


def delete_employee(employee_id: int) -> bool:
    employee = get_employee(employee_id)

    if employee is None:
        return False

    employees.remove(employee)

    return True
