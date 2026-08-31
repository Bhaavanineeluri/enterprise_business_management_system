from pydantic import BaseModel


class CSVImportResponse(BaseModel):
    success: bool
    message: str
    total_rows: int
    imported_rows: int
    failed_rows: int
    errors: list[str]
