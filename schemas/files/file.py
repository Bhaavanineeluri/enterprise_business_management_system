from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    stored_filename: str
    file_path: str
    content_type: str | None
    file_size: int
    uploaded_by: int
    created_at: datetime
    updated_at: datetime


class FileMessageResponse(BaseModel):
    success: bool
    message: str
    data: FileResponse
