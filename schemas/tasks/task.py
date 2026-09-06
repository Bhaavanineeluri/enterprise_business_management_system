from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    task_code: str = Field(..., min_length=2, max_length=50)
    title: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    assigned_to: int | None = Field(default=None, gt=0)
    priority: str = Field(
        default="medium",
        min_length=2,
        max_length=20,
    )
    status: str = Field(
        default="pending",
        min_length=2,
        max_length=30,
    )
    due_date: datetime | None = None

    @field_validator(
        "task_code",
        "title",
        "description",
        "priority",
        "status",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip().lower() if value in {
                "low",
                "medium",
                "high",
                "pending",
                "in_progress",
                "completed",
                "cancelled",
            } else value.strip()
        return value


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    description: str | None = None
    assigned_to: int | None = Field(default=None, gt=0)
    priority: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )
    status: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    due_date: datetime | None = None

    @field_validator(
        "title",
        "description",
        "priority",
        "status",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value):
        if isinstance(value, str):
            return value.strip().lower() if value in {
                "low",
                "medium",
                "high",
                "pending",
                "in_progress",
                "completed",
                "cancelled",
            } else value.strip()
        return value


class TaskPatch(TaskUpdate):
    pass


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_code: str
    title: str
    description: str | None
    assigned_to: int | None
    priority: str
    status: str
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime


class TaskSingleResponse(BaseModel):
    success: bool
    message: str
    data: TaskResponse


class TaskListData(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int


class TaskListResponse(BaseModel):
    success: bool
    message: str
    data: TaskListData
