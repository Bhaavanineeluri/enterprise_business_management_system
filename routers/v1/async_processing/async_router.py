from fastapi import APIRouter, BackgroundTasks

from services.async_processing.async_service import process_async_task


router = APIRouter(
    prefix="/async-processing",
    tags=["Async Processing"],
)


@router.post("/tasks")
def create_async_task(
    task_name: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        process_async_task,
        task_name,
    )

    return {
        "message": "Task added to background processing",
        "task_name": task_name,
        "status": "processing",
    }
