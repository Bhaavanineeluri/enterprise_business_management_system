from math import ceil

from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.employees.employee import Employee
from models.users.user import User
from schemas.search.search import SearchResponse, SearchResult


SEARCH_TYPES = {
    "user",
    "employee",
}


def search_records(
    db: Session,
    query: str,
    record_type: str = "all",
    page: int = 1,
    page_size: int = 20,
    sort_order: str = "desc",
) -> SearchResponse:

    if page < 1:
        raise ValueError(
            "page must be greater than or equal to 1"
        )

    if not 1 <= page_size <= 100:
        raise ValueError(
            "page_size must be between 1 and 100"
        )

    if record_type != "all" and record_type not in SEARCH_TYPES:
        raise ValueError(
            "type must be one of: all, user, employee"
        )

    if sort_order not in {"asc", "desc"}:
        raise ValueError(
            "sort_order must be either asc or desc"
        )

    keyword = query.strip()

    if not keyword:
        raise ValueError(
            "q must not be empty"
        )

    results: list[SearchResult] = []

    if record_type in {"all", "user"}:

        users = (
            db.query(User)
            .filter(
                User.is_active.is_(True),
                or_(
                    User.username.ilike(
                        f"%{keyword}%"
                    ),
                    User.email.ilike(
                        f"%{keyword}%"
                    ),
                    User.role.ilike(
                        f"%{keyword}%"
                    ),
                ),
            )
            .all()
        )

        results.extend(
            SearchResult(
                id=user.id,
                type="user",
                title=user.username,
                subtitle=user.email,
                created_at=user.created_at,
            )
            for user in users
        )

    if record_type in {"all", "employee"}:

        employees = (
            db.query(Employee)
            .filter(
                Employee.deleted_at.is_(None),
                or_(
                    Employee.employee_code.ilike(
                        f"%{keyword}%"
                    ),
                    Employee.full_name.ilike(
                        f"%{keyword}%"
                    ),
                    Employee.email.ilike(
                        f"%{keyword}%"
                    ),
                ),
            )
            .all()
        )

        results.extend(
            SearchResult(
                id=employee.id,
                type="employee",
                title=employee.full_name,
                subtitle=employee.email,
                created_at=employee.created_at,
            )
            for employee in employees
        )

    results.sort(
        key=lambda item: item.created_at or 0,
        reverse=sort_order == "desc",
    )

    total = len(results)

    start = (page - 1) * page_size
    end = start + page_size

    paginated_results = results[start:end]

    total_pages = (
        ceil(total / page_size)
        if total
        else 0
    )

    return SearchResponse(
        results=paginated_results,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )
