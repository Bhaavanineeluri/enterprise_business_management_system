from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.tasks.task import (
    TaskCreate,
    TaskListResponse,
    TaskPatch,
    TaskSingleResponse,
    TaskUpdate,
)
from services.tasks.task_service import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    restore_task,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskSingleResponse, status_code=status.HTTP_201_CREATED)
def create_task_api(
    task_data: TaskCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    task = create_task(db, task_data)
    response.headers["Location"] = f"/api/v1/tasks/{task.id}"
    return {
        "success": True,
        "message": "Task created successfully",
        "data": task,
    }


@router.get("", response_model=TaskListResponse)
def get_tasks_api(
    assigned_to: int | None = Query(default=None, gt=0),
    priority: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    task_code: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size

    tasks, total = get_tasks(
        db,
        assigned_to=assigned_to,
        priority=priority,
        status=status_filter,
        task_code=task_code,
        offset=offset,
        limit=page_size,
    )

    pages = ((total + page_size - 1) // page_size) if total else 0

    return {
        "success": True,
        "message": "Tasks retrieved successfully",
        "data": {
            "items": tasks,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        },
    }


@router.get("/{task_id}", response_model=TaskSingleResponse)
def get_task_api(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {
        "success": True,
        "message": "Task retrieved successfully",
        "data": task,
    }


@router.put("/{task_id}", response_model=TaskSingleResponse)
def update_task_api(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = update_task(db, task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {
        "success": True,
        "message": "Task updated successfully",
        "data": task,
    }


@router.patch("/{task_id}", response_model=TaskSingleResponse)
def patch_task_api(
    task_id: int,
    task_data: TaskPatch,
    db: Session = Depends(get_db),
):
    task = update_task(db, task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {
        "success": True,
        "message": "Task partially updated successfully",
        "data": task,
    }


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_task(db, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{task_id}/restore", response_model=TaskSingleResponse)
def restore_task_api(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = restore_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted task not found",
        )

    return {
        "success": True,
        "message": "Task restored successfully",
        "data": task,
    }
