from fastapi import Query


def pagination_params(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of records per page",
    ),
) -> dict[str, int]:
    return {
        "page": page,
        "page_size": page_size,
    }
