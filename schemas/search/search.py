from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    title: str
    subtitle: str | None = None
    created_at: datetime | None = None


class SearchResponse(BaseModel):
    results: list[SearchResult]
    page: int
    page_size: int
    total: int
    total_pages: int
