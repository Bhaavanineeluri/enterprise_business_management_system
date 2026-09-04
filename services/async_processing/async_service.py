import time


def process_async_task(task_name: str) -> dict:
    print(f"Background task started: {task_name}")

    time.sleep(5)

    print(f"Background task completed: {task_name}")

    return {
        "task_name": task_name,
        "status": "completed",
    }
