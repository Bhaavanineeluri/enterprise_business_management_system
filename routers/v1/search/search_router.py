from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.search.search import SearchResponse
from services.search.search_service import search_records


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get(
    "/",
    response_model=SearchResponse,
)
def search(
    q: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="Keyword to search for",
    ),
    type: str = Query(
        default="all",
        pattern="^(all|user|employee|file)$",
        description="Resource type to search",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of results per page",
    ),
    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$",
        description="Sort by creation date",
    ),
    db: Session = Depends(get_db),
):
    return search_records(
        db=db,
        query=q,
        record_type=type,
        page=page,
        page_size=page_size,
        sort_order=sort_order,
    )
